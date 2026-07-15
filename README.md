# HPCA 2027 I-Fuse Workloads

This repository is the single installation entry point for the final I-Fuse
workload set. It keeps the Git repository small and downloads validated,
replay-ready SimPoint trace bundles from immutable Hugging Face dataset
revisions.

## Install

Install the workload entry point from Hugging Face:

```bash
python3 -m pip install -U huggingface_hub
hf download harry1332/hpca2027-ifuse-workloads \
  --type dataset --local-dir hpca2027-ifuse-workloads
cd hpca2027-ifuse-workloads
./install.sh
```

Or clone the GitHub mirror:

```bash
git clone https://github.com/wumingzh-cmu-S26/hpca2027-ifuse-workloads.git
cd hpca2027-ifuse-workloads
./install.sh
```

Install every workload:

```bash
./install.sh
```

Install selected workloads or a group:

```bash
./install.sh appworld leveldb rocksdb
./install.sh agentic
./install.sh database
./install.sh datacenter
```

Use `./install.sh --list` to show every canonical name and source. Use
`--output PATH` to choose the installation directory. Installed workload names
are stable symlinks into `.workload-cache`, so repeated installation does not
duplicate trace ZIP data.

## Canonical Workloads

| Install name | Pinned source folder | Category |
|---|---|---|
| `appworld` | `appworld` | Agentic |
| `bc` | `bc` | Graph |
| `bfs` | `bfs` | Graph |
| `core_bench` | `core_bench_tomography_3497606` | Agentic |
| `dfs` | `dfs` | Graph |
| `leveldb` | `leveldb_readrandom` | Database |
| `mlgym_fmnist` | `mlgym_fmnist` | Agentic |
| `pagerank` | `pagerank` | Graph |
| `rocksdb` | `rocksdb_readrandom` | Database |
| `sssp_ego_fb` | `sssp_ego_fb` | Graph |
| `terminal_bench` | `terminalbench_train_fasttext` | Agentic |

`datacenter` is a Scarab suite/group name, not a standalone trace in the
current workload database. In this installer it expands to `bc`, `bfs`, `dfs`,
`pagerank`, `rocksdb`, and `sssp_ego_fb`. If the final list intended a specific
datacenter benchmark, add its concrete trace name to `workloads.json` rather
than assigning a fabricated bundle to that alias.

The final evaluation set intentionally excludes TaoBench and DuckDB. TaoBench
was used only as an engineering smoke test for the runtime I-Fuse mechanism;
neither workload should appear in final speedup results.

## Validation

Every install verifies that the downloaded bundle contains:

- `trace_clustering_info.json`
- selected SimPoint and weight files
- at least one replay-ready `traces_simp/trace/*.zip`

The manifest pins full Hugging Face commit revisions. Run the local consistency
check with:

```bash
python3 verify_manifest.py
python3 verify_remote.py
python3 -m unittest discover -s tests
```
