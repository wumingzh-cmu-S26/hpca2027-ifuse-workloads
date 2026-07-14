#!/usr/bin/env python3
"""Install pinned HPCA 2027 I-Fuse trace bundles from Hugging Face."""

import argparse
import json
import os
import shutil
from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "workloads.json"


def load_manifest() -> dict:
    with MANIFEST.open() as source:
        manifest = json.load(source)
    if manifest.get("schema_version") != 1:
        raise SystemExit("Unsupported workload manifest schema")
    return manifest


def expand_names(requested: list[str], manifest: dict) -> list[str]:
    workloads = manifest["workloads"]
    groups = manifest["groups"]
    expanded: list[str] = []
    for name in requested:
        if name in groups:
            candidates = groups[name]
        elif name in workloads:
            candidates = [name]
        else:
            choices = ", ".join(sorted(set(workloads) | set(groups)))
            raise SystemExit(f"Unknown workload or group {name!r}. Choices: {choices}")
        for candidate in candidates:
            if candidate not in expanded:
                expanded.append(candidate)
    return expanded


def validate_bundle(path: Path, expected_name: str) -> int:
    required = (
        path / "trace_clustering_info.json",
        path / "simpoints" / "opt.p.lpt0.99",
        path / "simpoints" / "opt.w.lpt0.99",
        path / "traces_simp" / "trace",
    )
    missing = [str(item) for item in required if not item.exists()]
    if missing:
        raise RuntimeError(f"{expected_name}: missing required bundle paths: {missing}")
    traces = sorted((path / "traces_simp" / "trace").glob("*.zip"))
    if not traces:
        raise RuntimeError(f"{expected_name}: no selected SimPoint trace ZIPs")
    with (path / "trace_clustering_info.json").open() as source:
        info = json.load(source)
    if not info.get("workload"):
        raise RuntimeError(f"{expected_name}: missing workload in clustering metadata")
    return len(traces)


def replace_symlink(link: Path, target: Path) -> None:
    if link.is_symlink():
        link.unlink()
    elif link.exists():
        raise RuntimeError(f"Refusing to replace non-symlink path: {link}")
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(os.path.relpath(target, start=link.parent), target_is_directory=True)


def install(name: str, entry: dict, output: Path, cache: Path) -> None:
    repo_dir = cache / entry["repo_id"].replace("/", "--") / entry["revision"]
    snapshot_download(
        repo_id=entry["repo_id"],
        repo_type="dataset",
        revision=entry["revision"],
        allow_patterns=[f'{entry["path"]}/**'],
        local_dir=repo_dir,
    )
    source = repo_dir / entry["path"]
    count = validate_bundle(source, name)
    replace_symlink(output / name, source)
    print(f"installed {name}: {count} selected trace(s) -> {output / name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "names",
        nargs="*",
        default=["all"],
        help="workloads or groups; defaults to all",
    )
    parser.add_argument("--output", type=Path, default=ROOT / "workloads")
    parser.add_argument("--cache", type=Path, default=ROOT / ".workload-cache")
    parser.add_argument("--list", action="store_true", help="list pinned workloads")
    args = parser.parse_args()

    manifest = load_manifest()
    if args.list:
        for name, entry in manifest["workloads"].items():
            print(f'{name:20} {entry["category"]:10} {entry["repo_id"]}/{entry["path"]}')
        print("groups:")
        for name, members in manifest["groups"].items():
            print(f"  {name}: {', '.join(members)}")
        return

    names = expand_names(args.names, manifest)
    args.output.mkdir(parents=True, exist_ok=True)
    args.cache.mkdir(parents=True, exist_ok=True)
    for name in names:
        install(name, manifest["workloads"][name], args.output, args.cache)


if __name__ == "__main__":
    main()
