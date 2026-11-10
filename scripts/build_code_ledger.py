#!/usr/bin/env python3
"""Generate _data/code_ledger.json for the availability overview table.

The repository manifest snapshot in ``_data/repo_manifests.json`` is captured
from the contents API. To keep the ledger compact we store the first page of
each listing (page size below); the availability flag is computed from that
same preview that the overview table displays.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_SIZE = 32
SIGNATURE_FILES = ["requirements.txt", "src/model.py", "src/rollout.py", "src/train.py"]


def preview_page(files):
    return files[:PAGE_SIZE]


def build():
    manifests = json.loads((ROOT / "_data/repo_manifests.json").read_text(encoding="utf-8"))
    index = json.loads((ROOT / "_data/project_index.json").read_text(encoding="utf-8"))
    projects = []
    for slug, info in index.items():
        repo = info.get("repo")
        files = manifests.get(slug)
        if not repo:
            status, page, missing = "missing", [], list(SIGNATURE_FILES)
        elif files == []:
            status, page, missing = "empty", [], list(SIGNATURE_FILES)
        else:
            page = preview_page(files)
            missing = [sig for sig in SIGNATURE_FILES if sig not in page]
            status = "pending" if missing else "released"
        total = len(files) if files else 0
        pages = max(1, math.ceil(total / PAGE_SIZE))
        projects.append(
            {
                "project": slug,
                "repo": repo,
                "status": status,
                "files_previewed": f"{len(page)} of {total}",
                "pages": f"1/{pages}",
                "preview_last": page[-1] if page else None,
                "signature_missing": missing,
            }
        )
    ledger = {
        "generated_by": "scripts/build_code_ledger.py",
        "as_of": "2026-11-08",
        "page_size": PAGE_SIZE,
        "projects": projects,
    }
    out = ROOT / "_data/code_ledger.json"
    out.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(projects)} projects)")


if __name__ == "__main__":
    build()
