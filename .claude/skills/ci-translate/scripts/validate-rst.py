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
import re
import subprocess
import sys
from pathlib import Path
from collections import Counter


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


def extract_structure(lines: list[str]) -> dict[str, list[tuple]]:
    """提取 RST 文件的结构元素"""
    directive_re = re.compile(r'^(?P<indent>\s*)\.\.\s+(?P<name>[A-Za-z0-9][A-Za-z0-9:-]*)::(?P<arg>.*)$')
    target_re = re.compile(r'^\.\.\s+_(?P<label>[^:]+):\s*$')
    option_re = re.compile(r'^(?P<indent>\s+):(?P<name>[A-Za-z0-9][A-Za-z0-9_-]*):(?P<value>.*)$')
    role_re = re.compile(r':(?P<name>[A-Za-z0-9][A-Za-z0-9:-]*):`(?P<body>[^`]+)`')
    literal_re = re.compile(r'``([^`\n]+)``')
    substitution_re = re.compile(r'(?<!\|)\|([A-Za-z0-9_.-]+)\|(?!\|)')

    data: dict[str, list[tuple]] = {
        'headings': [],
        'heading_levels': [],
        'directives': [],
        'targets': [],
        'options': [],
        'roles': [],
        'literals': [],
        'substitutions': [],
        'potential_translated_directives': [],
        'fullwidth_double_colons': [],  # 检测全角双冒号：
    }

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

    return data


def compare_sequence(name: str, source: list[tuple], translated: list[tuple]) -> list[str]:
    """比较序列是否一致"""
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


def check_spacing_norms(lines: list[str]) -> list[str]:
    """检查中英文间距规范"""
    errors: list[str] = []
    chinese_char = r'[\u4e00-\u9fff]'
    english_char = r'[a-zA-Z0-9]'

    in_code_block = False

    for i, line in enumerate(lines, start=1):
        # 检测代码块开始/结束
        if line.strip().startswith('.. code-block::'):
            in_code_block = True
        elif in_code_block and line.strip() and not line.startswith('    ') and not line.startswith('\t'):
            in_code_block = False

        # 跳过代码块内的检查
        if in_code_block or line.startswith('    ') or line.startswith('\t'):
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
    translated = extract_structure(translated_lines)
    errors: list[str] = []

    # 检查标题装饰线
    for lineno, title, mark, length, _has_overline in translated['headings']:
        if length < len(title):
            errors.append(
                f'标题装饰线过短：第 {lineno + 1} 行长度 {length} < 标题长度 {len(title)}（标题：{title!r}，装饰符：{mark!r}）'
            )

    # 检查是否有疑似被误译的指令
    for lineno, directive_name, text in translated['potential_translated_directives']:
        errors.append(f'🚨 疑似指令被误译为普通文本（第 {lineno} 行）：{text!r}')

    # 检查是否有全角双冒号（段落结尾的 :: 被误译为中文冒号 ：）
    for lineno, _colon_type, text in translated['fullwidth_double_colons']:
        errors.append(f'🚨 发现全角双冒号（第 {lineno} 行）：{text!r} - 段落结尾的 RST 代码块标记"::"不能翻译为"："，必须保持半角冒号')

    # 如果有备份文件，进行对比
    if backup_path.exists():
        source_lines = read_lines(backup_path)
        source = extract_structure(source_lines)

        errors.extend(compare_sequence('标题层级', source['heading_levels'], translated['heading_levels']))
        directive_errors = compare_all_directives(source, translated)
        errors.extend(directive_errors)
        errors.extend(compare_sequence('显式目标', source['targets'], translated['targets']))
        errors.extend(compare_sequence('选项', source['options'], translated['options']))
        errors.extend(compare_sequence('交叉引用角色', source['roles'], translated['roles']))
        errors.extend(compare_literal_presence(source['literals'], translated['literals']))
        errors.extend(compare_sequence('替换引用', source['substitutions'], translated['substitutions']))

        critical_errors = compare_critical_directives(source, translated)
        if critical_errors:
            errors = critical_errors + errors

    # 检查间距规范（不阻断）
    spacing_errors = check_spacing_norms(translated_lines)

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
