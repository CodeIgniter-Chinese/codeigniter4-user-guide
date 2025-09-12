# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概览

这是 **CodeIgniter 4 用户指南中文翻译项目** - 一个社区驱动的项目，旨在为 CodeIgniter PHP 框架提供高质量的中文文档。项目使用 Sphinx 和 RestructuredText 格式，并保持严格的翻译标准。

**当前版本**：CodeIgniter v4.6.3
**语言**：简体中文
**技术栈**：Python + Sphinx + RestructuredText

## 核心架构

### 目录结构
- `source/` - RestructuredText (.rst) 格式的主要文档源文件
- `build/` - 生成的文档输出（HTML、PDF）
- `.claude/agents/` - AI 翻译代理配置
- `.github/workflows/` - 构建和部署的 CI/CD 自动化

### 关键组件
- **Sphinx 配置**：`source/conf.py` 定义构建设置、中文语言支持和扩展
- **翻译标准**：记录在 `translation-guide.md` 和 AI 代理配置中
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

### Docker 工作流
```bash
# 构建容器
docker build -t ci4 .

# 生成文档
docker run -t --rm -v $(pwd):/ci ci4
```

## 依赖关系 (requirements.txt)

- **Sphinx** (>=5.3.0, <6.0.0) - 文档生成器
- **sphinx-rtd-theme** (>=2.0.0, <3.0.0) - Read the Docs 主题
- **sphinxcontrib-phpdomain** (>=0.11.0) - PHP 语法高亮
- **jieba** (==0.42.1) - 中文分词
- **docutils** (>=0.19) - RestructuredText 处理

## 翻译工作流

### AI 辅助翻译
- 使用专业的 Claude 代理（`codeigniter-translator`）进行一致性翻译
- 代理配置位于 `.claude/agents/codeigniter-translator.md`
- 在确保自然中文表达的同时保持技术准确性

### 质量标准
- **格式保留**：RestructuredText 语法必须保持完整
- **术语一致性**：CodeIgniter 特定术语遵循既定约定
- **中文排版**：严格遵守中文文案排版指北
- **代码保留**：所有代码块和技术示例保持英文

### 翻译规则
- **核心术语**：框架组件（Session、Email、BaseController）保持英文
- **标准翻译**："helper" → "辅助函数"，"library" → "库"，"controller" → "控制器"
- **间距**：中英文/数字之间添加空格
- **标点**：中文句子使用全角标点符号

## CI/CD 流水线

### 自动化构建 (.github/workflows/build.yml)
- **触发条件**：推送到 master 分支
- **环境**：Ubuntu 22.04 + Python 3.7
- **LaTeX 支持**：使用 XeLaTeX 和中文字体的完整中文排版
- **输出**：HTML 文档 + PDF 生成
- **部署**：自动部署到 GitHub Pages

### 构建流程
1. 安装 Python 依赖和中文支持的 LaTeX 包
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
- 始终运行 `make html` 验证 RestructuredText 语法
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
- **表格**：保持列对齐和 RST 表格语法完整

### 中文语言约定
- 使用非正式的"你"而不是正式的"您"
- 删除不必要的代词以获得更自然的中文表达
- 在中文字符与英文/数字之间添加适当间距
- 中文句子使用全角标点（，。！？）

## AI 团队配置

### 专业代理
- **codeigniter-translator**：CodeIgniter 文档翻译专家，深度掌握 RestructuredText 格式和中文技术写作标准
- **codeigniter-translation-reviewer**：翻译质量保证代理，用于审查已完成的翻译

### 使用方法
- 所有新翻译工作使用翻译代理
- 提交前使用审查代理验证翻译质量
- 代理理解项目特定的术语和格式要求