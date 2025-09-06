# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Chinese translation of the CodeIgniter 4 User Guide, built using Sphinx documentation system. The project translates English CodeIgniter 4 documentation into Chinese using ReStructuredText (.rst) format.

## Essential Commands

### Building Documentation
```bash
# Install dependencies (requires Python 3.5+)
pip install -r requirements.txt

# Build HTML documentation
make html

# Build PDF documentation
make latexpdf

# Clean build artifacts
make clean
```

### Docker Development
```bash
# Build and run in Docker container
docker build -t codeigniter4-user-guide .
docker run --rm -v $(pwd):/app -w /app codeigniter4-user-guide make html
```

## Architecture

### Directory Structure
- **`source/`**: All ReStructuredText documentation files
  - `conf.py`: Sphinx configuration with Chinese language settings
  - `index.rst`: Master document tree defining site structure
  - Topic directories: `tutorial/`, `installation/`, `concepts/`, `database/`, `libraries/`, `helpers/`
  - `_static/`: CSS, JavaScript, images, and other assets
  - `_templates/`: Custom Sphinx templates
- **`build/`**: Generated documentation output
  - `html/`: Web-ready HTML files
  - `doctrees/`: Sphinx build cache

### Key Technologies
- **Sphinx 5.3.0+**: Static site generator optimized for technical documentation
- **ReStructuredText**: Markup format for all content files
- **sphinxcontrib-phpdomain**: PHP syntax highlighting and cross-referencing
- **sphinx-rtd-theme**: Read the Docs theme
- **jieba**: Chinese text segmentation for search functionality

### Build System
The project uses a standard Sphinx Makefile workflow:
1. RST files in `source/` are processed by Sphinx
2. Chinese language configuration in `source/conf.py`
3. Output generated to `build/html/` or `build/latex/`
4. GitHub Actions automates builds and deploys to GitHub Pages

## Translation Guidelines

When editing documentation:
- Follow Chinese copywriting standards defined in `translation-guide.md`
- Maintain consistency with existing terminology
- Preserve RST markup structure and Sphinx directives
- Test builds locally before committing: `make html`
- Use signed commits as required by project workflow

## CI/CD Pipeline

GitHub Actions automatically:
- Builds HTML and PDF versions on master branch pushes
- Deploys HTML to GitHub Pages
- Uses LaTeX/XeTeX for proper Chinese PDF generation
- Validates all builds before deployment

## Development Workflow

1. Edit RST files in appropriate `source/` subdirectories
2. Run `make html` to build and preview locally in `build/html/`
3. Check `build/html/index.html` in browser to verify changes
4. For PDF testing, run `make latexpdf` (requires LaTeX installation)
5. Commit with signed-off commits following project conventions

## Common File Patterns

- Documentation pages: `source/**/*.rst`
- Configuration: `source/conf.py`
- Static assets: `source/_static/**/*`
- Templates: `source/_templates/**/*`
- Build output: `build/**/*` (git-ignored)