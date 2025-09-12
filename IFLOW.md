# CodeIgniter 4 中文用户指南项目

## 项目概述

这是一个 CodeIgniter 4 中文用户指南的翻译项目，旨在为中文开发者提供完整的 CodeIgniter 4 框架文档。该项目使用 Sphinx 文档系统构建，生成 HTML、PDF 等多种格式的文档。

项目托管在 GitHub 上，使用 GitHub Actions 自动构建和部署到 GitHub Pages。

## 项目类型

这是一个技术文档翻译项目，基于 ReStructuredText (RST) 格式的文档源文件，使用 Sphinx 构建系统生成最终文档。

## 目录结构

```
.
├── source/                 # 文档源文件目录
│   ├── index.rst           # 主页文档
│   ├── intro/              # 介绍部分
│   ├── installation/       # 安装指南
│   ├── tutorial/           # 教程
│   ├── concepts/           # 概念说明
│   ├── general/            # 通用主题
│   ├── incoming/           # 请求处理
│   ├── outgoing/           # 响应处理
│   ├── database/           # 数据库相关
│   ├── models/             # 模型相关
│   ├── dbmgmt/             # 数据库管理
│   ├── libraries/          # 库文档
│   ├── helpers/            # 辅助函数
│   ├── testing/            # 测试相关
│   ├── cli/                # 命令行接口
│   ├── extending/          # 扩展框架
│   └── changelogs/         # 更新日志
├── build/                  # 构建输出目录
│   ├── html/               # HTML 输出
│   └── latex/              # LaTeX 输出
├── _static/                # 静态资源文件
├── _templates/             # 模板文件
├── requirements.txt        # Python 依赖项
├── conf.py                 # Sphinx 配置文件
├── Makefile                # 构建脚本
├── Dockerfile              # Docker 配置
└── README.md               # 项目说明
```

## 构建和运行

### 依赖安装

```bash
# 安装 Python 依赖
pip install -r requirements.txt
```

### 本地构建

```bash
# 构建 HTML 文档
make html

# 构建 PDF 文档
make latexpdf
```

### Docker 构建

```bash
# 构建 Docker 镜像
docker build -t ci4 .

# 运行构建
docker run -t --rm -v $(pwd):/ci ci4
```

## 开发规范

### 翻译规范

1. 严格遵循[中文文案排版指北](http://mazhuang.org/wiki/chinese-copywriting-guidelines/)
2. 遵循项目特定的[文档翻译指南](translation-guide.md)
3. 使用"你"而非"您"
4. 保持技术术语的一致性
5. 保留 ReStructuredText 格式结构

### ReStructuredText 格式要求

1. 保留所有 RST 指令（如 `.. note::`, `.. warning::` 等）
2. 保持代码块内容为英文
3. 保持交叉引用链接为英文
4. 保留表格和列表结构

### 术语翻译标准

- "helper" → "辅助函数"
- "library" → "库"
- "model" → "模型"
- "controller" → "控制器"
- "view" → "视图"
- "route/routing" → "路由"

## 贡献指南

1. Fork 主仓库
2. 翻译完成后自己 Review 两遍
3. 提交 PR 并使用 --signoff 签名
4. 遵循中文文案排版规范

## 自动化流程

- 使用 GitHub Actions 自动构建文档
- 构建结果部署到 GitHub Pages
- 生成 HTML 和 PDF 两种格式

## 配置文件说明

- `conf.py`: Sphinx 配置文件，包含主题、语言、扩展等设置
- `requirements.txt`: Python 依赖项列表
- `Makefile`: 构建脚本
- `Dockerfile`: Docker 构建配置

## 构建环境要求

- Python 3.7+
- Sphinx 5.3.0+
- TeXLive (用于生成 PDF)

## 预览地址

[在线预览最新文档](https://codeigniter-chinese.github.io/codeigniter4-user-guide/)
