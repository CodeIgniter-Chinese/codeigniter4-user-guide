#!/usr/bin/env python3
import json
import re
import sys

DANGEROUS = [
    (r"\brm\s+-rf\b", "禁止 rm -rf（翻译流程不需要）"),
    (r"\bgit\s+reset\s+--hard\b", "禁止 git reset --hard（高风险破坏性操作）"),
    (r"\bgit\s+clean\s+-f", "禁止 git clean -f（高风险删除文件）"),
    (r"\bcurl\b.*\|\s*(sh|bash)\b", "禁止 curl|bash（供应链风险）"),
    (r"\bwget\b.*\|\s*(sh|bash)\b", "禁止 wget|bash（供应链风险）"),
    (r"\bsudo\b", "禁止 sudo（翻译流程不应需要提权）"),
]

def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        eprint(f"[hook] Invalid JSON input: {e}")
        return 1

    if data.get("tool_name") != "Bash":
        return 0

    tool_input = data.get("tool_input", {}) or {}
    cmd = tool_input.get("command", "") or ""
    if not cmd.strip():
        return 0

    for pattern, reason in DANGEROUS:
        if re.search(pattern, cmd, flags=re.IGNORECASE | re.DOTALL):
            eprint(
                "[ci-translate hook] 已阻止危险 Bash 命令：\n"
                f"  {cmd}\n"
                f"原因：{reason}\n"
                "请改用更安全的替代方式，或仅运行本流程所需命令（mkdir/python/git diff/status）。"
            )
            return 2

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
