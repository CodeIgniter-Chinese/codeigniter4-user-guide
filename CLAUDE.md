# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概览

这是 **CodeIgniter 4 用户指南中文翻译项目** — 一个社区驱动的项目，旨在为 CodeIgniter PHP 框架提供高质量的中文文档。项目使用 Sphinx 和 RestructuredText 格式，并保持严格的翻译标准。

**当前版本**：CodeIgniter v4.6.3
**语言**：简体中文
**技术栈**：Python + Sphinx + RestructuredText

## 核心架构

### 目录结构
- `source/` — RestructuredText (.rst) 格式的主要文档源文件，按主题分子目录（`libraries/`、`general/`、`database/`、`cli/`、`models/` 等）
- `build/` — 生成的文档输出（HTML、PDF），不在版本控制中
- `.claude/skills/ci-translate/` — AI 翻译 skill，包含翻译工作流、验证脚本和示例
- `.github/workflows/` — 构建和部署的 CI/CD 自动化

### 关键组件
- **Sphinx 配置**：`source/conf.py` 定义构建设置、中文语言支持（`zh_CN`）、主题和扩展
- **翻译标准**：记录在 `translation-guide.md` 和 ci-translate skill 中
- **构建系统**：基于 Makefile，支持 Docker 以保证环境一致性

## 构建命令

### 本地开发
```bash
# 安装依赖
pip install -r requirements.txt

# 构建 HTML 文档
make html

# 构建 PDF 文档
make latexpdf

# 查看生成的文档
# HTML 文件位于 build/html/
# PDF 文件位于 build/latex/CodeIgniter.pdf
```

### 翻译单个文件
```bash
# 使用 ci-translate skill 翻译单个 .rst 文件
/ci-translate source/libraries/caching.rst

# 或者手动验证单个 .rst 文件的语法
python3 .claude/skills/ci-translate/scripts/validate-rst.py source/libraries/caching.rst
```

### Docker 工作流
```bash
# 构建容器
docker build -t ci4 .

# 生成文档
docker run -t --rm -v $(pwd):/ci ci4
```

## 依赖关系

### Python 依赖 (requirements.txt)
- **Sphinx** (>=5.3.0, <6.0.0) — 文档生成器
- **sphinx-rtd-theme** (>=2.0.0, <3.0.0) — Read the Docs 主题
- **sphinxcontrib-phpdomain** (>=0.11.0) — PHP 语法高亮
- **jieba** (==0.42.1) — 中文分词
- **docutils** (>=0.19) — RestructuredText 处理

### 开发工具
- **esbonio** — RST Language Server Protocol 支持，配置在 `pyproject.toml` 中，使用项目的 `.venv` 虚拟环境
- **validate-rst.py** — 位于 `.claude/skills/ci-translate/scripts/` 的 RST 语法验证脚本

## 翻译工作流

### ci-translate Skill
这是项目的主要翻译工具，实现完整的翻译闭环：

```bash
/ci-translate source/libraries/caching.rst
```

**工作流步骤**：
1. 备份英文原文到 `$FILE_PATH.en.bak`
2. 翻译 RST 为中文（遵守格式保留、术语一致、中文表达规则）
3. 运行 `validate-rst.py` 校验 RST 语法
4. 进行静态审查（格式、代码块、术语、翻译腔）
5. 生成审查报告
6. 按报告修订并复验
7. 定稿并删除备份

**核心翻译规则**：
- **格式零破坏**：reST 指令（`.. note::`）、角色（`:doc:`）、代码块、字面量保持英文
- **代码不翻译**：代码块、类名、方法名、配置键、URL 完全保持英文
- **信息零遗漏**：版本限定、语气强度、条件前提必须完整保留
- **消除翻译腔**：删除冗余代词（你/它/这），拆分长句，主动语态
- **术语一致**：helper → 辅助函数，validation → 验证，controller → 控制器

### 质量标准
- **格式保留**：RestructuredText 语法必须保持完整
- **术语一致性**：遵循 `translation-guide.md` 和 ci-translate skill 中的术语表
- **中文排版**：严格遵守中文文案排版指北（中英文间距、全角标点）
- **代码保留**：所有代码块和技术示例保持英文

## CI/CD 流水线

### 自动化构建 (.github/workflows/build.yml)
- **触发条件**：推送到 master 分支
- **环境**：Ubuntu 22.04 + Python 3.7
- **LaTeX 支持**：使用 XeLaTeX 和中文字体的完整中文排版
- **输出**：HTML 文档 + PDF 生成
- **部署**：自动部署到 GitHub Pages（gh-pages 分支）

### 构建流程
1. 安装 Python 依赖和中文支持的 LaTeX 包（texlive-xetex、texlive-lang-chinese）
2. 生成 HTML 和 PDF 文档
3. 将 HTML 部署到 GitHub Pages 分支
4. 复制 PDF 到部署目录

## 贡献指南

### 文件编辑
- 仅编辑 `source/` 目录下的 `.rst` 文件
- 保持 RestructuredText 格式和缩进的精确性
- 绝不翻译代码块、类名或方法名
- 遵循中文文案排版标准的间距和标点规范

### 测试更改
- 使用 `make html` 验证 RestructuredText 语法
- 检查 `build/html/` 中生成的 HTML 格式问题
- 确保中文文本使用正确字体正常渲染

### 代码审查
- 所有翻译都需要审查技术准确性
- 验证相关文档部分的术语一致性
- 检查交叉引用和内部链接是否正常工作

## 文档标准

### RestructuredText 元素
- **指令**：保持 `.. note::`、`.. warning::`、`.. code-block::` 不翻译
- **交叉引用**：维持 `:doc:`、`:meth:`、`:class:` 链接目标为英文
- **代码块**：保持精确缩进，绝不翻译内容
- **段落尾冒号**：`::` 表示代码块，严禁改为中文冒号
- **表格**：保持列对齐和 RST 表格语法完整

### 中文语言约定
- 使用非正式的"你"而不是正式的"您"
- 删除不必要的代词以获得更自然的中文表达
- 在中文字符与英文/数字之间添加适当间距（半角空格）
- 中文句子使用全角标点（，。！？）
- 数字与单位之间不加空格（如 50ms）

## 参考资源

- **translation-guide.md** — 翻译标准和术语指南
- **.claude/skills/ci-translate/examples/** — 翻译示例和常见错误模式
- **.claude/skills/ci-translate/templates/** — 审查报告模板
- **预览站点**：https://codeigniter-chinese.github.io/codeigniter4-user-guide/
