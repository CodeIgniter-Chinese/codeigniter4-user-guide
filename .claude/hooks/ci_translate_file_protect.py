#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        eprint(f"[hook] Invalid JSON input: {e}")
        return 1

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path")

    if tool not in ("Write", "Edit"):
        return 0
    if not file_path:
        return 0

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
    p = Path(file_path)
    abs_p = (project_dir / p).resolve() if not p.is_absolute() else p.resolve()

    # 项目外一律阻止
    try:
        abs_p.relative_to(project_dir)
    except ValueError:
        eprint(
            "[ci-translate hook] 拒绝写入项目外路径：\n"
            f"  {abs_p}\n"
            "请仅修改仓库内文件。"
        )
        return 2

    rel = abs_p.relative_to(project_dir)

    # 永远允许写入工作目录
    if str(rel).startswith(".ci-translation-tmp") or str(rel).startswith(".ci-translation-backups"):
        return 0

    # 永远禁止触碰敏感路径
    if str(rel).startswith(".git") or rel.name in (".env",):
        eprint(
            "[ci-translate hook] 拒绝写入敏感路径：\n"
            f"  {rel}\n"
            "这类文件不应在翻译流程中被修改。"
        )
        return 2

    # 只对 .rst 源文档做保护
    if rel.suffix.lower() != ".rst":
        return 0

    meta = project_dir / ".ci-translation-tmp" / ".ci-translate-meta.json"
    if not meta.exists():
        eprint(
            "[ci-translate hook] 未找到本次会话 meta 文件：\n"
            f"  {meta}\n"
            "请先按命令的“预检查”步骤生成 backup_ts。"
        )
        return 2

    try:
        meta_obj = json.loads(meta.read_text(encoding="utf-8"))
        backup_ts = meta_obj.get("backup_ts")
    except Exception as e:
        eprint(f"[ci-translate hook] 读取 meta 失败：{e}")
        return 2

    if not backup_ts:
        eprint("[ci-translate hook] meta 中缺少 backup_ts，无法确认备份目录。")
        return 2

    backup_root = project_dir / ".ci-translation-backups" / backup_ts
    if not backup_root.exists():
        eprint(
            "[ci-translate hook] 未找到备份目录（禁止覆盖源 .rst）：\n"
            f"  {backup_root}\n"
            "请先成功执行备份步骤。"
        )
        return 2

    # 进一步：检查该文件的备份是否存在（按相对路径保存的前提）
    backup_file = backup_root / rel
    if not backup_file.exists():
        eprint(
            "[ci-translate hook] 未找到该文件对应备份（禁止覆盖源 .rst）：\n"
            f"  目标：{rel}\n"
            f"  期望备份：{backup_file}\n"
            "请确认 ci_backup.py 按相对路径保存，或调整 hook 以匹配实际备份布局。"
        )
        return 2

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
