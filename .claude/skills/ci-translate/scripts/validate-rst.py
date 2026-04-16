#!/usr/bin/env python3
"""
RST 格式验证脚本

用于检查翻译后的 RST 文件是否保持了关键 reST/Sphinx 结构。

功能：
1. 检查标题装饰线长度
2. 检查指令数量和类型
3. 检查关键指令（warning/note 等）
4. 检查交叉引用和角色
5. 检查表格格式
6. 检查中英文间距规范
7. 运行 Sphinx 构建（可选）
"""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
from pathlib import Path
from collections import Counter

from docutils.core import publish_doctree
from docutils import nodes


# 关键指令：这些指令如果被删除会导致语义变化
# 基于 https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html

# Docutils 标准警告指令（admonitions）
DOCUTILS_ADMONITIONS = {
    'attention', 'caution', 'danger', 'error', 'hint', 'important', 'note', 'tip', 'warning', 'admonition'
}

# Sphinx 特有指令
SPHINX_DIRECTIVES = {
    # 版本变更指令
    'versionadded', 'versionchanged', 'deprecated', 'versionremoved',
    # 呈现指令
    'seealso', 'rubric', 'centered', 'hlist',
    # 元信息指令
    'sectionauthor', 'codeauthor',
    # 索引指令
    'index', 'no-index', 'noindex',
    # 条件内容
    'only',
    # 其他 Sphinx 特有
    'glossary', 'productionlist', 'tabularcolumns', 'math',
}

# 代码相关指令
CODE_DIRECTIVES = {
    'code-block', 'sourcecode', 'literalinclude', 'highlight',
}

# 内容指令
CONTENT_DIRECTIVES = {
    'contents', 'toctree', 'include', 'raw', 'class', 'role',
    'table', 'csv-table', 'list-table',
    'image', 'figure', 'topic', 'sidebar',
}

# 所有关键指令合集
CRITICAL_DIRECTIVES = DOCUTILS_ADMONITIONS | SPHINX_DIRECTIVES | CODE_DIRECTIVES | CONTENT_DIRECTIVES

# 关键指令可能被误译成的普通文本模式
CRITICAL_DIRECTIVE_TEXT_PATTERNS = {
    'attention': re.compile(r'^\s*(?:注意|关注)[：:]'),
    'caution': re.compile(r'^\s*谨慎[：:]'),
    'danger': re.compile(r'^\s*危险[：:]'),
    'error': re.compile(r'^\s*(?:错误|ERROR)[：:]'),
    'hint': re.compile(r'^\s*提示[：:]'),
    'important': re.compile(r'^\s*重要[：:]'),
    'note': re.compile(r'^\s*(?:注意|备注|说明)[：:]'),
    'tip': re.compile(r'^\s*(?:提示|技巧)[：:]'),
    'warning': re.compile(r'^\s*警告[：:]'),
    'seealso': re.compile(r'^\s*(?:参见|另请参阅|另见)[：:]'),
    'rubric': re.compile(r'^\s*(?:标题|题注)[：:]'),
    'glossary': re.compile(r'^\s*词汇表[：:]'),
}

# 检测段落结尾双冒号被翻译成全角冒号的模式
# 在 RST 中，段落以 :: 结尾表示后续缩进内容为代码块/文字块
FULLWIDTH_DOUBLE_COLON_PATTERN = re.compile(r'：：\s*$')  # 行尾全角双冒号

DIRECTIVE_ARGS_MUST_MATCH = {
    'code-block',
    'literalinclude',
    'include',
    'image',
    'figure',
    'php:namespace',
    'php:class',
    'php:method',
    'php:function',
    'php:attr',
    'php:trait',
    'php:interface',
}

DIRECTIVE_VERSION_PREFIX = {'versionadded', 'versionchanged', 'deprecated'}
OPTION_VALUES_MUST_MATCH = {'depth', 'local', 'lines', 'linenos', 'start-after', 'end-before', 'emphasize-lines'}

TITLE_MARKS = set('=-~^"\'`+*#')

# Docutils 原生支持的指令
DOCUTILS_DIRECTIVES = {
    'attention', 'caution', 'danger', 'error', 'hint', 'important',
    'note', 'tip', 'warning', 'admonition',
    'image', 'figure', 'topic', 'sidebar',
    'contents', 'rubric', 'table',
    'math', 'parsed-literal', 'code',
    'csv-table', 'list-table',
}


# ============================================================
# AST 解析引擎
# ============================================================

def _suppress_stderr(func):
    """在调用会产⽣ system_message 的解析时抑制 stderr"""
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        return func()
    finally:
        sys.stderr = old_stderr


def _parse_directive_from_rawsource(rawsource: str) -> str | None:
    """从 rawsource 中提取指令名称"""
    match = re.match(r'^\s*\.\.\s+([A-Za-z0-9][A-Za-z0-9:-]*)::', rawsource)
    if match:
        return match.group(1)
    return None


def _extract_ast_directives(text: str) -> Counter:
    """
    使用 docutils AST 解析 RST 文本，提取所有指令类型。

    处理三种情况：
    1. docutils 原生指令（warning, note, image 等）→ AST 节点直接遍历
    2. 未知指令（toctree, literalinclude, php:class 等）→ 从 system_message 的 rawsource 提取
    3. 静默指令（contents）→ 从原始文本的 rawsource 提取

    返回指令类型计数器。
    """
    counts: Counter = Counter()

    def _parse():
        return publish_doctree(text)

    doctree = _suppress_stderr(_parse)

    # 1. 遍历 AST 找 docutils 原生指令节点
    for node in doctree.traverse():
        tagname = getattr(node, 'tagname', '')

        # Admonition 指令
        if tagname in DOCUTILS_ADMONITIONS:
            counts[tagname] += 1
        # image / figure / topic / sidebar
        elif tagname in ('image', 'figure', 'topic', 'sidebar', 'table'):
            counts[tagname] += 1

    # 2. 从 system_message 中提取未知指令
    #    docutils 对未知指令会产生 ERROR/3 system_message，
    #    其子节点包含一个 literal_block，rawsource 保留原始 RST 文本
    for msg in doctree.traverse(nodes.system_message):
        if msg.get('type') == 'ERROR' and msg.get('level') == 3:
            # 检查段落文本是否包含 "Unknown directive type"
            for child in msg.children:
                if isinstance(child, nodes.paragraph):
                    para_text = child.astext()
                    if 'Unknown directive type' in para_text or 'Unknown directive' in para_text:
                        # 从 literal_block 子节点的 rawsource 提取指令名
                        for lc in msg.children:
                            if isinstance(lc, nodes.literal_block):
                                name = _parse_directive_from_rawsource(lc.rawsource)
                                if name:
                                    counts[name] += 1
                                break

    # 3. 从 code-block literal_block 的 classes 识别 code-block
    for lb in doctree.traverse(nodes.literal_block):
        classes = lb.get('classes', [])
        if 'code' in classes:
            counts['code-block'] += 1

    # 4. 从原始文本提取 contents（静默指令，不在 AST 中留节点）
    #    用正则匹配 .. contents::
    for match in re.finditer(r'^\.\.\s+contents::', text, re.MULTILINE):
        counts['contents'] += 1

    return counts


def _extract_ast_roles(text: str) -> Counter:
    """
    使用 docutils AST 解析 RST 文本，提取所有角色。

    Sphinx 角色（:doc:、:ref:、:php:class: 等）在 docutils 中会产生
    problematic 节点和 system_message。从 rawsource 中提取角色名。
    """
    counts: Counter = Counter()

    # 方法：从文本中用正则匹配 :name:`...` 或 :domain:name:`...` 模式
    # docutils 不会正确解析 Sphinx 角色，但 rawsource 保留了原始文本
    role_pattern = re.compile(r':([A-Za-z][A-Za-z0-9_-]*(?::[A-Za-z][A-Za-z0-9_-]*)?):`')
    for match in role_pattern.finditer(text):
        counts[match.group(1)] += 1

    return counts


def read_lines(path: Path) -> list[str]:
    """读取文件所有行"""
    return path.read_text(encoding='utf-8').splitlines()


def normalize_role_body(body: str) -> str:
    """标准化角色体"""
    body = body.strip()
    match = re.match(r'(?P<text>.+?)\s*<(?P<target>[^<>]+)>\s*$', body)
    if match:
        return f"<{match.group('target').strip()}>"
    return body


def extract_multiline_roles(lines: list[str]) -> list[tuple[int, str, str]]:
    """
    检测跨两行的 Sphinx 角色。

    Sphinx 角色可能因行宽限制被拆分为两行，如::

        :doc:`all
        supported database systems <../intro/requirements>`

    这类角色在逐行扫描时无法被 role_re 匹配。本函数将相邻两行拼接后
    重新匹配，找到跨行角色后返回（行号为起始行）。
    """
    roles: list[tuple[int, str, str]] = []
    # 匹配 :name:`text` 且 `text` 未闭合（有开头的 ` 但行尾没有对应的 `）
    open_role_re = re.compile(r':([A-Za-z0-9][A-Za-z0-9:-]*):`(?P<body>[^`]*)$')
    # 匹配以 ` 结尾的角色体（补全行）
    close_role_re = re.compile(r'^(?P<prefix>[^`]*)`')

    for i in range(len(lines) - 1):
        line_curr = lines[i].rstrip()
        line_next = lines[i + 1].rstrip()

        match = open_role_re.search(line_curr)
        if match is None:
            continue

        # 当前行以未闭合的角色开始
        role_name = match.group(1)
        body_part1 = match.group('body')

        # 下一行应该有闭合的 `
        close_match = close_role_re.search(line_next)
        if close_match is None:
            continue

        body_part2 = close_match.group('prefix')
        full_body = body_part1 + body_part2

        # 验证完整角色体是否包含目标引用 <...> 或普通文本
        lineno = i + 1  # 1-based
        roles.append((lineno, role_name, normalize_role_body(full_body)))

    return roles


def extract_structure(lines: list[str]) -> dict[str, list[tuple]]:
    """提取 RST 文件的结构元素"""
    directive_re = re.compile(r'^(?P<indent>\s*)\.\.\s+(?P<name>[A-Za-z0-9][A-Za-z0-9:-]*)::(?P<arg>.*)$')
    target_re = re.compile(r'^\.\.\s+_(?P<label>[^:]+):\s*$')
    option_re = re.compile(r'^(?P<indent>\s+):(?P<name>[A-Za-z0-9][A-Za-z0-9_-]*):(?P<value>.*)$')
    role_re = re.compile(r':(?P<name>[A-Za-z0-9][A-Za-z0-9:-]*):`(?P<body>[^`]+)`')
    literal_re = re.compile(r'``([^`\n]+)``')
    substitution_re = re.compile(r'(?<!\|)\|([A-Za-z0-9_.-]+)\|(?!\|)')
    # 角色行内匹配：用于在选项判断中排除角色
    inline_role_re = re.compile(r'^\s+:[A-Za-z][A-Za-z0-9_-]*:`')
    # 列表项提取：有序 (1. 2. 等) 和无序 (* + - 等)
    list_item_re = re.compile(r'^(?P<indent>\s*)(?P<marker>\d+\.|[*+\-])\s+')

    data: dict[str, list[tuple]] = {
        'headings': [],
        'heading_levels': [],
        'directives': [],
        'targets': [],
        'options': [],
        'roles': [],
        'literals': [],
        'substitutions': [],
        'list_items': [],
        'potential_translated_directives': [],
        'fullwidth_double_colons': [],  # 检测全角双冒号：
    }

    # 收集所有 literal_block 的行号范围（用于排除代码块内的检查）
    code_block_ranges: list[tuple[int, int]] = _find_code_block_ranges(lines)

    for lineno, line in enumerate(lines, start=1):
        stripped = line.rstrip()

        directive_match = directive_re.match(stripped)
        if directive_match:
            name = directive_match.group('name')
            arg = directive_match.group('arg').lstrip()
            key = None
            if name in DIRECTIVE_ARGS_MUST_MATCH:
                key = arg
            elif name in DIRECTIVE_VERSION_PREFIX:
                key = arg.split()[0] if arg else ''
            data['directives'].append((lineno, len(directive_match.group('indent')), name, key))

        target_match = target_re.match(stripped)
        if target_match:
            data['targets'].append((lineno, target_match.group('label')))

        option_match = option_re.match(line)
        if option_match:
            if not inline_role_re.match(line):
                name = option_match.group('name')
                value = option_match.group('value').strip()
                key = value if name in OPTION_VALUES_MUST_MATCH else None
                data['options'].append((lineno, len(option_match.group('indent')), name, key))

        for match in role_re.finditer(line):
            data['roles'].append((lineno, match.group('name'), normalize_role_body(match.group('body'))))

        for match in literal_re.finditer(line):
            data['literals'].append((lineno, match.group(1)))

        if not stripped.lstrip().startswith('.. '):
            for match in substitution_re.finditer(line):
                data['substitutions'].append((lineno, match.group(1)))

        # 提取列表项
        list_match = list_item_re.match(line)
        if list_match:
            indent = len(list_match.group('indent'))
            marker_type = 'ordered' if list_match.group('marker').endswith('.') else 'unordered'
            data['list_items'].append((lineno, indent, marker_type))

        # 检测可能被误译为普通文本的关键指令
        for directive_name, pattern in CRITICAL_DIRECTIVE_TEXT_PATTERNS.items():
            if pattern.match(stripped):
                data['potential_translated_directives'].append((lineno, directive_name, stripped[:50]))

        # 检测全角双冒号（段落结尾的 :: 被误译为中文冒号 ：）
        # 注意：只检测明确的全角双冒号，单个全角冒号是正常中文标点
        if FULLWIDTH_DOUBLE_COLON_PATTERN.search(stripped):
            data['fullwidth_double_colons'].append((lineno, 'fullwidth_double', stripped[:50]))

    # 检查标题
    for index in range(len(lines) - 1):
        title = lines[index].rstrip()
        underline = lines[index + 1].rstrip()

        if not title or title.startswith((' ', '\t')):
            continue
        if not underline or len(set(underline)) != 1 or underline[0] not in TITLE_MARKS:
            continue

        has_overline = False
        if index > 0:
            overline = lines[index - 1].rstrip()
            has_overline = bool(
                overline
                and len(set(overline)) == 1
                and overline[0] == underline[0]
            )

        data['headings'].append((index + 1, title, underline[0], len(underline), has_overline))
        data['heading_levels'].append((index + 1, underline[0], has_overline))

    # 存储代码块范围供外部使用
    data['_code_block_ranges'] = code_block_ranges

    # 补充检测跨两行的角色（逐行扫描无法匹配的情况）
    multiline_roles = extract_multiline_roles(lines)
    data['roles'].extend(multiline_roles)
    # 按行号排序以保持顺序
    data['roles'].sort(key=lambda t: t[0])

    return data


def _find_code_block_ranges(lines: list[str]) -> list[tuple[int, int]]:
    """
    使用 AST 方式识别所有 literal_block（代码块）的行号范围。

    包括 code-block 指令块和 :: 引导的代码块。
    返回 [(start_lineno, end_lineno), ...] 列表（1-based）。
    """
    ranges: list[tuple[int, int]] = []
    i = 0
    n = len(lines)

    while i < n:
        stripped = lines[i].strip()
        lineno_0 = i  # 0-based

        # 检测 code-block / literalinclude 等指令
        if stripped.startswith('.. ') and ('::' in stripped):
            directive_match = re.match(r'^\.\.\s+([A-Za-z0-9][A-Za-z0-9:-]*)::', stripped)
            if directive_match:
                name = directive_match.group(1)
                if name in ('code-block', 'sourcecode', 'literalinclude'):
                    # 找到指令起始，继续找指令结束（空行或新指令）
                    indent_match = re.match(r'^(\s*)', lines[i])
                    base_indent = len(indent_match.group(1)) if indent_match else 0
                    # 寻找选项（缩进 > base_indent 的行）
                    j = i + 1
                    while j < n:
                        line_stripped = lines[j].strip()
                        if not line_stripped:
                            j += 1
                            continue
                        line_indent = len(re.match(r'^\s*', lines[j]).group(0))
                        if line_indent <= base_indent:
                            break
                        j += 1
                    # 对于 literalinclude，选项之后可能还有内容，但主要是选项部分
                    # 对于 code-block，选项之后是代码内容（更深缩进）
                    if name == 'literalinclude':
                        # literalinclude 没有行内代码，只检查选项
                        ranges.append((lineno_0 + 1, j))
                    else:
                        # code-block 的内容在更深缩进的行中
                        content_start = j
                        while j < n:
                            line_stripped = lines[j].strip()
                            if not line_stripped:
                                j += 1
                                continue
                            line_indent = len(re.match(r'^\s*', lines[j]).group(0))
                            # 内容缩进必须比 base_indent + 4 更深（或至少比 base_indent 深）
                            if line_indent <= base_indent + 3:
                                break
                            j += 1
                        ranges.append((lineno_0 + 1, j))
                    i = j
                    continue

        # 检测段落结尾 :: 引导的代码块
        if stripped.endswith('::') and len(stripped) > 2:
            # 后续缩进行都是代码
            j = i + 1
            while j < n:
                line_stripped = lines[j].strip()
                if not line_stripped:
                    j += 1
                    continue
                line_indent = len(re.match(r'^\s*', lines[j]).group(0))
                if line_indent < 4:
                    break
                j += 1
            if j > i + 1:
                ranges.append((lineno_0 + 1, j))

        i += 1

    return ranges


def _is_in_code_block(lineno_1based: int, ranges: list[tuple[int, int]]) -> bool:
    """判断给定行号（1-based）是否在代码块范围内"""
    for start, end in ranges:
        if start <= lineno_1based <= end:
            return True
    return False


def compare_sequence(name: str, source: list[tuple], translated: list[tuple]) -> list[str]:
    """比较序列是否一致（适用于有序序列，如标题层级、目标标签）"""
    errors: list[str] = []

    if len(source) != len(translated):
        errors.append(f'{name} 数量不一致：源文 {len(source)}，译文 {len(translated)}')

    for index, (src, dst) in enumerate(zip(source, translated), start=1):
        if src[1:] != dst[1:]:
            errors.append(
                f'{name} 第 {index} 项不一致：源文第 {src[0]} 行 {src[1:]!r}；译文第 {dst[0]} 行 {dst[1:]!r}'
            )
            if len(errors) >= 20:
                break

    return errors


def _compare_heading_underlines(source: dict, translated: dict) -> list[str]:
    """
    对比标题装饰线长度是否与源文一致。

    译文装饰线长度应与源文相同，除非译文标题文本本身比源文装饰线更长，
    此时允许加长以覆盖标题。
    """
    errors: list[str] = []

    src_headings = source['headings']
    dst_headings = translated['headings']

    for (_src_ln, _src_title, _src_mark, src_len, _src_ol), \
        (dst_ln, dst_title, _dst_mark, dst_len, _dst_ol) in zip(src_headings, dst_headings):

        expected = src_len
        if len(dst_title) > src_len:
            expected = len(dst_title)

        if dst_len != expected:
            if dst_len > expected:
                errors.append(
                    f'标题装饰线过长：译文第 {dst_ln + 1} 行长度 {dst_len}，'
                    f'预期 {expected}（源文长度 {src_len}）'
                )
            else:
                errors.append(
                    f'标题装饰线过短：译文第 {dst_ln + 1} 行长度 {dst_len}，'
                    f'预期 {expected}（源文长度 {src_len}）'
                )

    return errors


def compare_set(name: str, source: list[tuple], translated: list[tuple],
                key_func=None) -> list[str]:
    """
    以集合方式对比无序元素（选项、字面量、替换引用等）。

    仅报告真正缺失或多余的项，而非位置错位产生的假阳性。

    Args:
        source: 源文元素列表
        translated: 译文元素列表
        key_func: 从元组中提取对比键的函数，默认使用元组[1:]切片
    """
    errors: list[str] = []
    if key_func is None:
        key_func = lambda t: t[1:]

    src_set = {key_func(t) for t in source}
    dst_set = {key_func(t) for t in translated}

    missing = src_set - dst_set
    extra = dst_set - src_set

    if missing:
        for item in list(missing)[:20]:
            src_lineno = next(t[0] for t in source if key_func(t) == item)
            errors.append(
                f'{name} 缺失：源文第 {src_lineno} 行包含 {item!r}，译文中未找到'
            )

    if extra:
        for item in list(extra)[:20]:
            dst_lineno = next(t[0] for t in translated if key_func(t) == item)
            errors.append(
                f'{name} 多余：译文第 {dst_lineno} 行包含 {item!r}，源文中不存在'
            )

    return errors


def compare_critical_directives(source: dict, translated: dict) -> list[str]:
    """专门检查关键指令是否被正确保留"""
    errors: list[str] = []

    source_critical = Counter(name for _lineno, _indent, name, _arg in source['directives'] if name in CRITICAL_DIRECTIVES)
    translated_critical = Counter(name for _lineno, _indent, name, _arg in translated['directives'] if name in CRITICAL_DIRECTIVES)

    all_critical_names = set(source_critical.keys()) | set(translated_critical.keys())
    for name in all_critical_names:
        source_count = source_critical.get(name, 0)
        translated_count = translated_critical.get(name, 0)
        if source_count != translated_count:
            if source_count > translated_count:
                errors.append(f'🚨 关键指令 "{name}" 数量不足：源文 {source_count} 个，译文 {translated_count} 个（缺失 {source_count - translated_count} 个，可能被误译为普通文本）')
            else:
                errors.append(f'🚨 关键指令 "{name}" 数量过多：源文 {source_count} 个，译文 {translated_count} 个（多出 {translated_count - source_count} 个，不能随意添加指令）')

    for lineno, directive_name, text in translated['potential_translated_directives']:
        found_as_directive = any(
            abs(d_lineno - lineno) <= 2 and d_name == directive_name
            for d_lineno, _indent, d_name, _arg in translated['directives'] if d_name in CRITICAL_DIRECTIVES
        )
        if not found_as_directive:
            errors.append(f'🚨 疑似关键指令 "{directive_name}" 被误译为普通文本（第 {lineno} 行）：{text!r}')

    return errors


def compare_all_directives(source: dict, translated: dict) -> list[str]:
    """检查所有指令的数量和类型必须与原文完全一致"""
    errors: list[str] = []

    source_directives = source['directives']
    translated_directives = translated['directives']

    if len(source_directives) != len(translated_directives):
        errors.append(f'🚨 指令总数不一致：源文 {len(source_directives)} 个，译文 {len(translated_directives)} 个')

    source_counts = Counter(name for _lineno, _indent, name, _arg in source_directives)
    translated_counts = Counter(name for _lineno, _indent, name, _arg in translated_directives)

    all_names = set(source_counts.keys()) | set(translated_counts.keys())
    for name in all_names:
        source_count = source_counts.get(name, 0)
        translated_count = translated_counts.get(name, 0)
        if source_count != translated_count:
            if source_count > translated_count:
                errors.append(f'🚨 指令 "{name}" 数量不足：源文 {source_count} 个，译文 {translated_count} 个')
            else:
                errors.append(f'🚨 指令 "{name}" 数量过多：源文 {source_count} 个，译文 {translated_count} 个（不能随意添加指令）')

    return errors


def compare_literal_presence(source: list[tuple], translated: list[tuple]) -> list[str]:
    """检查字面量是否存在"""
    errors: list[str] = []

    missing = [item for item in source if item[1] not in {value for _, value in translated}]
    for lineno, value in missing[:20]:
        errors.append(f'行内字面量缺失：源文第 {lineno} 行包含 {value!r}，译文中未找到')

    return errors


def compare_ast_directives(source_text: str, translated_text: str) -> list[str]:
    """使用 AST 对比源文和译文的指令数量"""
    errors: list[str] = []

    source_counts = _extract_ast_directives(source_text)
    translated_counts = _extract_ast_directives(translated_text)

    all_names = set(source_counts.keys()) | set(translated_counts.keys())
    for name in sorted(all_names):
        source_count = source_counts.get(name, 0)
        translated_count = translated_counts.get(name, 0)
        if source_count != translated_count:
            if source_count > translated_count:
                errors.append(
                    f'🚨 指令 "{name}" 数量不足：源文 {source_count} 个，译文 {translated_count} 个'
                    f'（缺失 {source_count - translated_count} 个，可能被误译为普通文本）'
                )
            else:
                errors.append(
                    f'🚨 指令 "{name}" 数量过多：源文 {source_count} 个，译文 {translated_count} 个'
                    f'（多出 {translated_count - source_count} 个，不能随意添加指令）'
                )

    return errors


def compare_ast_roles(source_text: str, translated_text: str) -> list[str]:
    """使用 AST 对比源文和译文的交叉引用角色数量"""
    errors: list[str] = []

    source_counts = _extract_ast_roles(source_text)
    translated_counts = _extract_ast_roles(translated_text)

    all_names = set(source_counts.keys()) | set(translated_counts.keys())
    for name in sorted(all_names):
        source_count = source_counts.get(name, 0)
        translated_count = translated_counts.get(name, 0)
        if source_count != translated_count:
            if source_count > translated_count:
                errors.append(
                    f'🚨 角色 :{name}: 数量不足：源文 {source_count} 个，译文 {translated_count} 个'
                    f'（缺失 {source_count - translated_count} 个）'
                )
            else:
                errors.append(
                    f'🚨 角色 :{name}: 数量过多：源文 {source_count} 个，译文 {translated_count} 个'
                    f'（多出 {translated_count - source_count} 个）'
                )

    return errors


def compare_literal_presence(source: list[tuple], translated: list[tuple]) -> list[str]:
    """检查字面量是否存在"""
    return compare_set('行内字面量', source, translated)


def compare_list_items(source: list[tuple], translated: list[tuple]) -> list[str]:
    """
    对比列表项结构。

    列表项使用 Counter 比较，既检查类型/缩进是否匹配，
    也检查数量是否一致。
    """
    errors: list[str] = []

    # 提取 (indent, marker_type) 的 Counter
    src_key = lambda t: (t[1], t[2])
    dst_key = lambda t: (t[1], t[2])

    from collections import Counter
    src_counter = Counter(src_key(t) for t in source)
    dst_counter = Counter(dst_key(t) for t in translated)

    if src_counter != dst_counter:
        # 找出差异
        all_keys = set(src_counter.keys()) | set(dst_counter.keys())
        for key in sorted(all_keys):
            src_count = src_counter.get(key, 0)
            dst_count = dst_counter.get(key, 0)
            if src_count != dst_count:
                indent, marker_type = key
                diff = src_count - dst_count
                if diff > 0:
                    errors.append(
                        f'列表项缺失：源文有 {src_count} 个 {marker_type} 列表项（缩进 {indent}），'
                        f'译文只有 {dst_count} 个'
                    )
                else:
                    errors.append(
                        f'列表项多余：译文有 {dst_count} 个 {marker_type} 列表项（缩进 {indent}），'
                        f'源文只有 {src_count} 个'
                    )

    return errors


def check_spacing_norms(lines: list[str], code_block_ranges: list[tuple[int, int]] = None) -> list[str]:
    """检查中英文间距规范"""
    errors: list[str] = []
    chinese_char = r'[\u4e00-\u9fff]'
    english_char = r'[a-zA-Z0-9]'

    # 确保 ranges 可用
    if code_block_ranges is None:
        code_block_ranges = _find_code_block_ranges(lines)

    for i, line in enumerate(lines, start=1):
        if _is_in_code_block(i, code_block_ranges):
            continue

        # 检查中文与英文之间是否有空格
        pattern1 = re.compile(f'({chinese_char})({english_char})')
        for match in pattern1.finditer(line):
            start_pos = match.start()
            if start_pos + 2 < len(line) and line[start_pos + 2] != ' ':
                if '``' not in line[max(0, start_pos-10):min(len(line), start_pos+10)]:
                    errors.append(f'中英文间距建议(第{i}行)："{match.group(0)}" 后建议加空格')

        # 检查数字与单位之间是否有多余空格
        pattern2 = re.compile(r'\d+\s+(ms|MB|GB|Gbps|GHz|KB|bytes?|seconds?|minutes?)\b')
        for match in pattern2.finditer(line):
            errors.append(f'数字与单位不应加空格(第{i}行)："{match.group(0)}"')

    return errors


def run_sphinx_build(file_path: Path) -> bool:
    """运行 Sphinx 构建"""
    try:
        # 查找项目根目录
        root_dir = file_path.parent
        while not (root_dir / 'Makefile').exists() and root_dir.parent != root_dir:
            root_dir = root_dir.parent

        if not (root_dir / 'Makefile').exists():
            print('💡 提示：未找到 Makefile，跳过构建验证。')
            return True

        # 查找虚拟环境
        venv_dir = root_dir / '.venv'
        if not venv_dir.exists():
            print('❌ 未找到虚拟环境 .venv，跳过构建验证。')
            print('   请先创建虚拟环境并安装依赖。')
            return False

        python_bin = venv_dir / 'bin' / 'python'
        if not python_bin.exists():
            print(f'❌ Python 解释器不存在：{python_bin}')
            return False

        print('运行 Sphinx 构建验证...')
        result = subprocess.run(
            ['make', '-C', str(root_dir), f'SPHINXBUILD={python_bin} -m sphinx', 'html'],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            print('✅ Sphinx 构建成功')
            return True
        else:
            print('❌ Sphinx 构建失败：')
            print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print('❌ 构建超时（超过 5 分钟）')
        return False
    except Exception as e:
        print(f'❌ 构建过程出错：{e}')
        return False


def main():
    parser = argparse.ArgumentParser(description='RST 文件格式验证工具')
    parser.add_argument('file', type=Path, help='要验证的 RST 文件路径')
    parser.add_argument('--no-build', action='store_true', help='跳过 Sphinx 构建')
    parser.add_argument('--verbose', action='store_true', help='详细输出')

    args = parser.parse_args()

    file_path = args.file

    # 检查文件是否存在
    if not file_path.exists():
        print(f'❌ 错误：文件不存在：{file_path}')
        sys.exit(1)

    if not file_path.is_file():
        print(f'❌ 错误：不是文件：{file_path}')
        sys.exit(1)

    # 查找备份文件
    backup_path = file_path.with_suffix(file_path.suffix + '.en.bak')

    print(f'=== RST 格式验证: {file_path} ===')
    if backup_path.exists():
        print(f'源文件备份: {backup_path}')
    else:
        print(f'⚠️  未找到源文件备份: {backup_path}')
        print('    将只执行单文件检查，无法比对英文源文结构。')
    print()

    # 读取文件
    translated_lines = read_lines(file_path)
    translated_text = '\n'.join(translated_lines)
    translated = extract_structure(translated_lines)
    errors: list[str] = []

    # 检查标题装饰线
    for lineno, title, mark, length, has_overline in translated['headings']:
        if length < len(title):
            errors.append(
                f'标题装饰线过短：第 {lineno + 1} 行长度 {length} < 标题长度 {len(title)}（标题：{title!r}，装饰符：{mark!r}）'
            )

    # 检查是否有疑似被误译的指令
    for lineno, text in translated['potential_translated_directives']:
        errors.append(f'🚨 疑似指令被误译为普通文本（第 {lineno} 行）：{text!r}')

    # 检查是否有全角双冒号（段落结尾的 :: 被误译为中文冒号 ：）
    for item in translated['fullwidth_double_colons']:
        lineno = item[0]
        text = item[2]  # item[1] is 'fullwidth_double' marker
        errors.append(f'🚨 发现全角双冒号（第 {lineno} 行）：{text!r} - 段落结尾的 RST 代码块标记"::"不能翻译为"："，必须保持半角冒号')

    # 如果有备份文件，进行对比
    if backup_path.exists():
        source_lines = read_lines(backup_path)
        source_text = '\n'.join(source_lines)
        source = extract_structure(source_lines)

        # --- AST 检查层：用 docutils 解析器做结构性校验 ---
        ast_errors = compare_ast_directives(source_text, translated_text)
        errors.extend(ast_errors)

        ast_role_errors = compare_ast_roles(source_text, translated_text)
        errors.extend(ast_role_errors)

        # --- 正则检查层：精确定位和特定检查 ---
        errors.extend(compare_sequence('标题层级', source['heading_levels'], translated['heading_levels']))
        errors.extend(_compare_heading_underlines(source, translated))
        directive_errors = compare_all_directives(source, translated)
        errors.extend(directive_errors)
        errors.extend(compare_sequence('显式目标', source['targets'], translated['targets']))

        errors.extend(compare_set('选项', source['options'], translated['options']))

        # 交叉引用角色：序列对比（角色顺序有意义）
        errors.extend(compare_sequence('交叉引用角色', source['roles'], translated['roles']))

        errors.extend(compare_set('行内字面量', source['literals'], translated['literals']))
        errors.extend(compare_set('替换引用', source['substitutions'], translated['substitutions']))

        errors.extend(compare_list_items(source['list_items'], translated['list_items']))

        critical_errors = compare_critical_directives(source, translated)
        if critical_errors:
            errors = critical_errors + errors

    # 检查间距规范（不阻断）
    spacing_errors = check_spacing_norms(translated_lines, translated.get('_code_block_ranges', []))

    # 输出错误
    if errors:
        critical = [e for e in errors if e.startswith('🚨')]
        normal = [e for e in errors if not e.startswith('🚨')]

        if critical:
            print()
            print('❌ 发现关键结构问题（必须修复）：')
            for error in critical[:20]:
                print(f'  {error}')

        if normal:
            print()
            print('❌ 发现可能破坏 RST/Sphinx 结构的问题：')
            for error in normal[:20]:
                print(f'  - {error}')

        if len(errors) > 20:
            print(f'  ... 其余 {len(errors) - 20} 项已省略')

    # 输出间距警告（不阻断）
    if spacing_errors:
        print()
        print('💡 发现排版优化建议（可选修复）：')
        for error in spacing_errors[:10]:
            print(f'  - {error}')
        if len(spacing_errors) > 10:
            print(f'  ... 其余 {len(spacing_errors) - 10} 项已省略')

    # 如果有错误，退出
    if errors:
        sys.exit(1)

    print('✅ 标题、指令、角色与字面量结构正常')

    # 运行构建（可选）
    if not args.no_build:
        if not run_sphinx_build(file_path):
            sys.exit(1)

    print()
    print('=== 验证完成 ===')

if __name__ == '__main__':
    main()
