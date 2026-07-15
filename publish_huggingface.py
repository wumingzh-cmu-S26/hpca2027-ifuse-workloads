#!/usr/bin/env python3
"""Publish the lightweight unified installer to its Hugging Face dataset repo."""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from huggingface_hub import HfApi, snapshot_download


ROOT = Path(__file__).resolve().parent
REPO_ID = "harry1332/hpca2027-ifuse-workloads"
FILES = (
    ".gitignore",
    "install.sh",
    "install_workloads.py",
    "requirements.txt",
    "verify_manifest.py",
    "verify_remote.py",
    "workloads.json",
)


def main() -> None:
    api = HfApi()
    account = api.whoami().get("name")
    if account != "harry1332":
        raise SystemExit(f"Unexpected Hugging Face account: {account!r}")

    api.create_repo(REPO_ID, repo_type="dataset", exist_ok=True, private=False)
    with tempfile.TemporaryDirectory() as temporary:
        staging = Path(temporary)
        shutil.copy2(ROOT / "huggingface" / "README.md", staging / "README.md")
        for name in FILES:
            shutil.copy2(ROOT / name, staging / name)
        api.upload_folder(
            folder_path=staging,
            repo_id=REPO_ID,
            repo_type="dataset",
            commit_message="Publish unified HPCA 2027 workload installer",
        )

    files = set(api.list_repo_files(REPO_ID, repo_type="dataset"))
    required = {"README.md", "install.sh", "install_workloads.py", "workloads.json"}
    missing = required - files
    if missing:
        raise SystemExit(f"Published repository is missing: {sorted(missing)}")
    info = api.repo_info(REPO_ID, repo_type="dataset")
    with tempfile.TemporaryDirectory() as temporary:
        checkout = Path(temporary) / "published"
        snapshot_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            revision=info.sha,
            local_dir=checkout,
        )
        subprocess.run([sys.executable, "verify_manifest.py"], cwd=checkout, check=True)
        subprocess.run(
            [sys.executable, "install_workloads.py", "--list"],
            cwd=checkout,
            check=True,
        )
    print(f"published {REPO_ID} at {info.sha}")


if __name__ == "__main__":
    main()
