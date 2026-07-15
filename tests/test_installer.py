import json
import tempfile
import unittest
from pathlib import Path

import install_workloads


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = install_workloads.load_manifest()

    def test_all_group_is_complete_and_unique(self) -> None:
        expanded = install_workloads.expand_names(["all"], self.manifest)
        self.assertEqual(set(expanded), set(self.manifest["workloads"]))
        self.assertEqual(len(expanded), len(set(expanded)))

    def test_groups_and_names_are_deduplicated(self) -> None:
        expanded = install_workloads.expand_names(
            ["database", "leveldb"], self.manifest
        )
        self.assertEqual(expanded, ["leveldb", "rocksdb"])

    def test_unknown_name_is_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            install_workloads.expand_names(["not-a-workload"], self.manifest)

    def test_validate_bundle_and_replace_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "source"
            (bundle / "simpoints").mkdir(parents=True)
            (bundle / "traces_simp" / "trace").mkdir(parents=True)
            (bundle / "trace_clustering_info.json").write_text(
                json.dumps({"workload": "test"})
            )
            (bundle / "simpoints" / "opt.p.lpt0.99").write_text("0 0\n")
            (bundle / "simpoints" / "opt.w.lpt0.99").write_text("1 0\n")
            (bundle / "traces_simp" / "trace" / "0.zip").write_bytes(b"zip")

            self.assertEqual(install_workloads.validate_bundle(bundle, "test"), 1)
            link = root / "installed" / "test"
            install_workloads.replace_symlink(link, bundle)
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), bundle.resolve())


if __name__ == "__main__":
    unittest.main()
