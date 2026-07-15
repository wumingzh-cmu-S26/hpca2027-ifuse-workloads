---
pretty_name: HPCA 2027 I-Fuse Workloads
license: other
task_categories:
  - other
tags:
  - computer-architecture
  - dynamorio
  - scarab
  - simpoint
  - hpca-2027
---

# HPCA 2027 I-Fuse Workloads

This dataset repository is the single installation entry point for the final
HPCA 2027 I-Fuse workload set. Its manifest pins validated trace bundles at
immutable commits across the existing Hugging Face datasets, avoiding duplicate
storage while preserving reproducibility.

## Install

```bash
python3 -m pip install -U huggingface_hub
hf download harry1332/hpca2027-ifuse-workloads \
  --type dataset --local-dir hpca2027-ifuse-workloads
cd hpca2027-ifuse-workloads
./install.sh
```

Install selected workloads or groups:

```bash
./install.sh appworld duckdb leveldb
./install.sh agentic
./install.sh database
./install.sh datacenter
```

Canonical concrete workloads are AppWorld, BC, BFS, CORE-Bench, DFS, DuckDB
TPC-H Q1 SF10, LevelDB readrandom, MLGym Fashion-MNIST, PageRank, RocksDB
readrandom, SSSP ego-Facebook, and Terminal-Bench FastText.

`datacenter` is a Scarab suite/group alias rather than a standalone trace. It
expands to BC, BFS, DFS, PageRank, RocksDB, and SSSP ego-Facebook.

Each installed bundle is checked for clustering metadata, selected SimPoint
files, weights, and replay-ready trace ZIPs. See `workloads.json` for exact
dataset revisions and source paths.
