#!/usr/bin/env python3
import json
import os
import shutil
import sys
from pathlib import Path

def safe_rmtree(path: Path, project_dir: Path):
    path = path.resolve()
    project_dir = project_dir.resolve()
    if project_dir not in path.parents:
        raise RuntimeError(f"Refuse to delete outside project: {path}")
    if path.name != ".ci-translation-tmp":
        raise RuntimeError(f"Refuse to delete non-tmp dir: {path}")
    if path.exists():
        shutil.rmtree(path)

def main():
    raw = sys.stdin.read().strip() or "{}"
    hook_input = json.loads(raw)

    if hook_input.get("stop_hook_active") is True:
        print(json.dumps({"decision": "approve", "suppressOutput": True}, ensure_ascii=False))
        return

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    tmp_dir = project_dir / ".ci-translation-tmp"
    result_path = tmp_dir / ".ci-translate-result.json"

    if not result_path.exists():
        print(json.dumps({"decision": "approve", "suppressOutput": True}, ensure_ascii=False))
        return

    result = json.loads(result_path.read_text(encoding="utf-8"))
    if result.get("status") != "success":
        print(json.dumps({"decision": "approve", "suppressOutput": True}, ensure_ascii=False))
        return

    backup_dir = project_dir / result["backup_dir"]
    files = result.get("files", [])

    backup_dir.mkdir(parents=True, exist_ok=True)

    summary_path = backup_dir / ".ci-translate-summary.md"
    summary_md = (
        "# 收尾总结\n\n"
        "## 1) ✅ 本次处理文件\n"
        + "".join([f"- {f}\n" for f in files]) + "\n"
        "## 2) 📦 备份位置\n"
        f"- 备份目录：`{backup_dir}`\n"
        f"- 临时目录：`{tmp_dir}`（已在成功后清理）\n\n"
        "## 3) 🧾 差异检查建议\n"
        "- `git status`\n"
        "- `git diff -- <FILE>`（逐个查看）\n\n"
        "## 4) 🔧 后续建议\n"
        "- 如项目有 Sphinx 构建：运行最轻量构建验证（尽量启用 warnings-as-errors）\n"
        "- 如需提交：建议按文件拆分 commit，便于 review\n"
    )
    summary_path.write_text(summary_md, encoding="utf-8")

    safe_rmtree(tmp_dir, project_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    print(json.dumps({
        "decision": "block",
        "reason": (
            "请继续一步：读取并原样输出以下文件内容（中文 Markdown）作为“收尾总结”，然后再停止：\n"
            f"{summary_path.as_posix()}"
        )
    }, ensure_ascii=False))

if __name__ == "__main__":
    main()
