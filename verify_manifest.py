#!/usr/bin/env python3
"""Validate internal consistency of the pinned workload manifest."""

import json
from pathlib import Path


root = Path(__file__).resolve().parent
with (root / "workloads.json").open() as source:
    manifest = json.load(source)

workloads = manifest["workloads"]
groups = manifest["groups"]
assert manifest["schema_version"] == 1
assert len(workloads) == 12
assert set(groups["all"]) == set(workloads)
assert len(groups["all"]) == len(set(groups["all"]))
for group, members in groups.items():
    unknown = set(members) - set(workloads)
    assert not unknown, f"{group}: unknown workloads {sorted(unknown)}"
for name, entry in workloads.items():
    assert entry["repo_id"].startswith("harry1332/")
    assert len(entry["revision"]) == 40
    assert entry["path"]
    assert entry["category"] in {"agentic", "database", "graph"}
print("manifest validation passed")
