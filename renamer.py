#!/usr/bin/env python
"""文件批量重命名工具。"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def collect_files(root: Path, exts: set[str]) -> list[Path]:
    files = [p for p in root.iterdir() if p.is_file()]
    if exts:
        files = [p for p in files if p.suffix.lower().lstrip(".") in exts]
    return sorted(files)


def build_new_name(old: Path, index: int, args) -> str:
    stem, suffix = old.stem, old.suffix
    if args.mode == "seq":
        return f"{args.prefix}{args.start + index:0{args.width}d}{suffix}"
    if args.mode == "date":
        ts = datetime.fromtimestamp(old.stat().st_mtime).strftime("%Y%m%d_%H%M%S")
        return f"{ts}_{index + 1:03d}{suffix}"
    if args.mode == "regex":
        if not args.pattern:
            raise ValueError("regex 模式需要 --pattern")
        return re.sub(args.pattern, args.replace or "", old.name)
    if args.mode == "lower":
        return old.name.lower()
    if args.mode == "upper":
        return old.name.upper()
    return old.name


def main() -> int:
    parser = argparse.ArgumentParser(description="文件批量重命名")
    parser.add_argument("directory", help="目标目录")
    parser.add_argument("--mode", required=True,
                        choices=["seq", "date", "regex", "lower", "upper"])
    parser.add_argument("--dry-run", action="store_true", help="只预览")
    parser.add_argument("--prefix", default="", help="序号模式前缀")
    parser.add_argument("--start", type=int, default=1, help="序号起始值")
    parser.add_argument("--width", type=int, default=3, help="序号位数")
    parser.add_argument("--pattern", help="正则表达式")
    parser.add_argument("--replace", help="替换内容")
    parser.add_argument("--ext", help="只处理指定扩展名，逗号分隔")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"[错误] 目录不存在: {root}")
        return 1

    exts = {e.strip().lower().lstrip(".") for e in args.ext.split(",")} if args.ext else set()
    files = collect_files(root, exts)
    if not files:
        print("没有找到符合条件的文件。")
        return 0

    planned: list[tuple[Path, Path]] = []
    used: set[str] = set()
    for i, old in enumerate(files):
        name = build_new_name(old, i, args)
        if name in used:
            name = f"{Path(name).stem}_{i}{Path(name).suffix}"
        used.add(name)
        planned.append((old, old.with_name(name)))

    for old, new in planned:
        mark = " " if old.name == new.name else "->"
        print(f"{old.name}  {mark}  {new.name}")

    if args.dry_run:
        print("\n[预览模式] 未修改任何文件。去掉 --dry-run 即可执行。")
        return 0

    for old, new in planned:
        if old.name != new.name:
            old.rename(new)
    print(f"\n完成，共处理 {len(planned)} 个文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())