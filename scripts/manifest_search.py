#!/usr/bin/env python3
"""Paginated search over the captured repository manifests.

The raw manifest snapshot can be large, so searches are printed one page at a
time. Always check the reported total and page count before drawing a
conclusion from the first page.
"""

import argparse
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--pattern", default=".")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--per-page", type=int, default=20)
    args = parser.parse_args()

    manifests = json.loads((ROOT / "_data/repo_manifests.json").read_text(encoding="utf-8"))
    files = manifests.get(args.project)
    if files is None:
        print(f"No manifest captured for project {args.project}.")
        return
    matches = [f for f in files if re.search(args.pattern, f)]
    total = len(matches)
    pages = max(1, math.ceil(total / args.per_page))
    page = min(max(1, args.page), pages)
    start = (page - 1) * args.per_page
    chunk = matches[start : start + args.per_page]
    print(f"Page {page}/{pages} | Total matches: {total}")
    for item in chunk:
        print(f"  {item}")


if __name__ == "__main__":
    main()
