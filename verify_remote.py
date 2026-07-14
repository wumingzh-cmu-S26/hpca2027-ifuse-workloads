#!/usr/bin/env python3
"""Verify every pinned workload source without downloading trace archives."""

import json
from collections import defaultdict
from pathlib import Path

from huggingface_hub import HfApi


root = Path(__file__).resolve().parent
with (root / "workloads.json").open() as source:
    manifest = json.load(source)

api = HfApi()
by_revision: dict[tuple[str, str], list[tuple[str, dict]]] = defaultdict(list)
for name, entry in manifest["workloads"].items():
    by_revision[(entry["repo_id"], entry["revision"])].append((name, entry))

for (repo_id, revision), entries in by_revision.items():
    files = set(api.list_repo_files(repo_id, repo_type="dataset", revision=revision))
    for name, entry in entries:
        prefix = entry["path"]
        required = {
            f"{prefix}/trace_clustering_info.json",
            f"{prefix}/simpoints/opt.p.lpt0.99",
            f"{prefix}/simpoints/opt.w.lpt0.99",
        }
        missing = required - files
        assert not missing, f"{name}: missing {sorted(missing)}"
        traces = sorted(
            path
            for path in files
            if path.startswith(f"{prefix}/traces_simp/trace/")
            and path.endswith(".zip")
        )
        assert traces, f"{name}: no selected trace ZIPs"
        print(f"verified {name}: {len(traces)} selected trace(s)")
