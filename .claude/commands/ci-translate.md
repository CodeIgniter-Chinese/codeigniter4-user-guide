---
description: CodeIgniter RST 英译中（备份→翻译→guard→审查报告→按报告修订→guard→覆盖），出版级质量，RST 保真（hooks 护栏）
argument-hint: [--dry-run] <file1.rst> [file2.rst ...]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(mkdir:*)
  - Bash(python scripts/*:*)
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(ls:*)
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/ci_translate_file_protect.py"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/ci_translate_bash_guard.py"
  Stop:
    - hooks:
        - type: command
          command: "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/ci_translate_stop_summary.py"
---

# 任务：CodeIgniter 文档英译中（逐文件串行，禁止并行）

目标文件：$ARGUMENTS

## 安全不变量（必须遵守）
1. 未成功备份前，绝不覆盖任何源文件。
2. 翻译初稿与修订终稿都必须写到 `.ci-translation-tmp/` 下；禁止直接写源 `.rst`。
3. 覆盖前必须 guard 通过：`python scripts/ci_rst_guard.py <SRC> <TMP>`；失败就停止并修复，不得覆盖。
4. 对每个文件：每个 guard 阶段最多允许 2 次“定点修复”重跑；仍失败则停止并报告具体违规点。
5. **原子性保证**：任一文件失败，立即停止处理后续文件

> hooks 护栏：Write/Edit 触及仓库内 `.rst` 源文件时，将强制检查 backup_ts 与备份存在性；不满足会直接阻止写入。

## 预检查（先做完再进入翻译）
- 若用户未传入至少 1 个文件路径：要求补充并停止。
- 对每个路径：确认存在且为普通文件（建议校验 `.rst` 后缀）。
- 创建目录（存在则忽略）：
  - `.ci-translation-backups/`
  - `.ci-translation-tmp/`
- 生成本次会话唯一 backup_ts，写入：
  - `.ci-translation-tmp/.ci-translate-meta.json`
  格式：`{"backup_ts":"YYYYMMDD-HHMMSS"}`
- **参数解析**：检查是否包含 --dry-run 参数
  - 如果包含：设置 DRY_RUN=true，从参数列表移除
  - 写入 .ci-translate-meta.json：{"backup_ts": "...", "dry_run": true}

## 子代理委派契约（必须遵守）
- 翻译初稿：使用显式句式
  - `Use the codeigniter-translator agent to ...`
- 审查：使用显式句式
  - `Use the codeigniter-translation-reviewer agent to ...`
- 若显式句式未触发委派，才允许使用 Task 工具兜底（不要手写 Task JSON）。

## 执行流程（逐文件处理）
对每个 FILE（按用户给出的顺序）：

### 1) 备份（强制使用本次 backup_ts）
- 从 `.ci-translation-tmp/.ci-translate-meta.json` 读取 backup_ts
- 运行：
  `python scripts/ci_backup.py --out .ci-translation-backups --timestamp <backup_ts> -- FILE`
- 确认备份目录 `.ci-translation-backups/<backup_ts>/` 已创建；否则停止。

### 2) 翻译初稿（写入 TMP）
- 读取 FILE 英文全文
- 计算 `TMP = .ci-translation-tmp/<与 FILE 相同的相对路径>`，确保父目录存在
- 委派 translator agent（使用自然语言描述，让 AI 自主执行）：
  "Use the codeigniter-translator agent to translate this CodeIgniter documentation from English to Chinese:

  [FILE 的完整英文内容]

  Note: This is an initial draft for guard validation."
- 将输出写入 TMP

### 3) Guard 校验（初稿）
- 运行：`python scripts/ci_rst_guard.py FILE TMP`
- 若失败：最多 2 次循环修复：
  - 把 guard 错误输出 + TMP 当前内容交给 translator
  - 要求“仅修复 guard 指出的违规点”，输出完整 RST
  - 重新写回 TMP 并重跑 guard
- 仍失败：停止并报告（不得覆盖源文件）

### 4) 审查（输出审查报告，不改文件）
- 委派审查：
  `Use the codeigniter-translation-reviewer agent to review the English source (FILE) and Chinese draft (TMP). Output ONLY a review report with actionable fixes.`
- 将报告保存为：`.ci-translation-tmp/<FILE 相对路径>.review.md`

### 5) 按审查报告修订（写回 TMP）
- 把：英文源全文 + TMP 当前中文全文 + 审查报告全文 交给 translator
- 要求：仅按报告逐条修订；保持 reST 结构零破坏；输出“最终修订后的完整 RST 内容”
- 将输出覆盖写回 TMP

### 6) Guard 校验（终稿）
- 运行：`python scripts/ci_rst_guard.py FILE TMP`
- 若失败：最多 2 次循环修复（同第 3 步，但这次也把 guard 错误 + 当前 TMP 给 translator 定点修复）
- 仍失败：停止并报告（不得覆盖源文件）

### 7) 覆盖源文件（条件执行）
- 读取 .ci-translate-meta.json 中的 dry_run 标志
- 如果 DRY_RUN=true：
  [输出]   ⊘ [干运行模式] 跳过覆盖
- 否则：用 TMP 覆盖 FILE
  [输出]   ✓ 覆盖完成

### 8) 写入成功标记（仅当全部文件都成功覆盖后）
- 写入：`.ci-translation-tmp/.ci-translate-result.json`
- 示例：
  {
    "status": "success",
    "backup_ts": "<backup_ts>",
    "backup_dir": ".ci-translation-backups/<backup_ts>/",
    "tmp_dir": ".ci-translation-tmp/",
    "files": [ ...按处理顺序... ]
  }
> 中途任何文件失败并停止：不要创建该文件。

## 收尾输出（中文）
- 输出本次处理的文件列表
- 输出备份根目录：`.ci-translation-backups/<backup_ts>/`
