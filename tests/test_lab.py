"""Fast stdlib-only tests. All Git writes and sprint clocks use temporary roots."""
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

from tools import lab


class LabTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="corrlaw-test-")
        self.root = Path(self.tmp.name)
        (self.root / "configs").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "src").mkdir()
        (self.root / ".research").mkdir()
        (self.root / "src/model.py").write_text("value = 1\n")
        (self.root / "docs/PROTOCOL.md").write_text("Status: DRAFT\n")
        (self.root / "configs/sprint.json").write_text(json.dumps({
            "budget_hours": 1, "report_reserve_minutes": 1,
            "max_threads": 2, "local_commits": True, "max_tracked_file_bytes": 20000}))
        (self.root / ".gitignore").write_text(".research/runtime/\nwork/\n.venv/\n")

    def tearDown(self):
        self.tmp.cleanup()

    def call(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return lab.main(["--root", str(self.root), *args])

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def initgit(self):
        if not shutil.which("git"):
            self.skipTest("Git not installed")
        self.git("init", "-q")
        self.git("config", "user.name", "Temporary Harness Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("add", "--", ".gitignore", "configs/sprint.json", "docs/PROTOCOL.md", "src/model.py")
        self.git("commit", "-qm", "fixture")

    def run_command(self, run_id, python_code, *extra):
        return self.call("run", "--id", run_id, "--task", "TEST",
                         "--purpose", "Harness test; not scientific evidence", "--timeout", "5",
                         *extra, "--", sys.executable, "-c", python_code)

    def test_inventory_excludes_generated_install_metadata(self):
        metadata = self.root / "src/corrlaw.egg-info"
        metadata.mkdir()
        (metadata / "PKG-INFO").write_text("generated metadata\n")
        (self.root / "src/.DS_Store").write_bytes(b"finder metadata")
        self.assertEqual(set(lab.inventory(self.root, ["src"])), {"src/model.py"})
        (self.root / "src/new_module.py").write_text("value = 2\n")
        self.assertIn("src/new_module.py", lab.inventory(self.root, ["src"]))

    def test_atomic_json_round_trip(self):
        p = self.root / "nested/one.json"
        lab.atomic(p, {"a": [1, 2]})
        self.assertEqual(lab.load(p), {"a": [1, 2]})
        self.assertEqual(list(p.parent.glob(".one.json.*")), [])

    def test_nonfinite_json_rejected(self):
        with self.assertRaises(ValueError):
            lab.atomic(self.root / "bad.json", {"x": float("nan")})

    def test_start_does_not_reset_budget(self):
        self.assertEqual(self.call("start"), 0)
        p = self.root / ".research/SPRINT.json"
        before = p.read_bytes()
        self.assertEqual(self.call("start"), 0)
        self.assertEqual(before, p.read_bytes())

    def test_paths_cannot_escape(self):
        for name in ("../secret", "/tmp/secret"):
            with self.assertRaises(lab.LabError):
                lab.inside(self.root, name)

    def test_symlinks_rejected(self):
        (self.root / "link").symlink_to(self.root / "src")
        with self.assertRaises(lab.LabError):
            lab.inside(self.root, "link/model.py")

    def test_ids_cannot_escape(self):
        for name in ("../x", "a/b", "", ".hidden", "a"*97):
            with self.assertRaises(lab.LabError):
                lab.valid_id(name)

    def test_run_requires_start(self):
        self.assertEqual(self.run_command("nostart", "print('x')"), 2)

    def test_success_records_provenance(self):
        self.call("start")
        self.assertEqual(self.run_command("success", "print('evidence')"), 0)
        record = lab.load(self.root / "results/runs/success/run.json")
        self.assertEqual(record["status"], "completed")
        self.assertEqual(record["result_validation"], "NOT_REVIEWED")
        self.assertTrue(record["log_sha256"])
        self.assertTrue((self.root / "results/runs/success/source_hashes.json").exists())
        self.assertIn("evidence", (self.root / record["log_path"]).read_text())

    def test_failed_command_preserved(self):
        self.call("start")
        self.assertEqual(self.run_command("failure", "raise SystemExit(7)"), 1)
        record = lab.load(self.root / "results/runs/failure/run.json")
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["returncode"], 7)

    def test_timeout(self):
        self.call("start")
        self.assertEqual(self.call("run", "--id", "timeout", "--task", "TEST", "--purpose", "timeout test",
                                   "--timeout", "1", "--", sys.executable, "-c", "import time; time.sleep(30)"), 1)
        record = lab.load(self.root / "results/runs/timeout/run.json")
        self.assertEqual(record["status"], "timed_out")
        self.assertLess(record["duration_seconds"], 10)

    def test_missing_executable_recorded(self):
        self.call("start")
        self.assertEqual(self.call("run", "--id", "missing", "--task", "TEST", "--purpose", "missing test",
                                   "--timeout", "2", "--", "certainly-no-such-corrlaw-executable-xyz"), 1)
        record = lab.load(self.root / "results/runs/missing/run.json")
        self.assertEqual(record["status"], "failed")
        self.assertTrue(record["error"])

    def test_duplicate_id_not_overwritten(self):
        self.call("start")
        self.run_command("once", "pass")
        path = self.root / "results/runs/once/run.json"
        before = path.read_bytes()
        self.assertEqual(self.run_command("once", "print('changed')"), 2)
        self.assertEqual(path.read_bytes(), before)

    def test_source_mutation_invalidates_run(self):
        self.call("start")
        code = "from pathlib import Path; Path('src/model.py').write_text('value = 2\\n')"
        self.assertEqual(self.run_command("changed", code), 1)
        self.assertEqual(lab.load(self.root / "results/runs/changed/run.json")["status"], "invalidated_source_changed")

    def test_source_addition_invalidates_run(self):
        self.call("start")
        code = "from pathlib import Path; Path('src/new.py').write_text('value = 3\\n')"
        self.assertEqual(self.run_command("added", code), 1)

    def test_confirmation_requires_freeze(self):
        self.call("start")
        self.assertEqual(self.run_command("unfrozen", "pass", "--phase", "confirmation"), 2)

    def test_reporting_reserve_blocks_new_experiments(self):
        self.call("start")
        path = self.root / ".research/SPRINT.json"
        record = lab.load(path)
        record["deadline_unix"] = time.time() + 20
        record["report_reserve_seconds"] = 60
        lab.atomic(path, record)
        self.assertEqual(self.run_command("too_late", "pass"), 2)
        self.assertEqual(self.run_command("audit", "pass", "--phase", "audit"), 0)

    def test_freeze_refuses_draft(self):
        self.initgit()
        self.assertEqual(self.call("freeze", "--id", "v1", "--paths", "src", "docs/PROTOCOL.md"), 2)

    def ready_freeze(self):
        (self.root / "docs/PROTOCOL.md").write_text("Status: READY_TO_FREEZE\n")
        self.initgit()
        self.assertEqual(self.call("freeze", "--id", "v1", "--paths", "src", "docs/PROTOCOL.md"), 0)

    def test_freeze_verification_and_immutability(self):
        self.ready_freeze()
        self.assertEqual(self.call("verify", "--id", "v1"), 0)
        self.assertEqual(self.call("freeze", "--id", "v1", "--paths", "src", "docs/PROTOCOL.md"), 2)

    def test_ready_header_cannot_hide_unresolved_protocol(self):
        (self.root / "docs/PROTOCOL.md").write_text("Status: READY_TO_FREEZE\nFinal metric: UNRESOLVED\n")
        self.initgit()
        self.assertEqual(self.call("freeze", "--id", "v1", "--paths", "src", "docs/PROTOCOL.md"), 2)

    def test_confirmation_accepts_matching_freeze(self):
        self.ready_freeze()
        self.call("start")
        self.assertEqual(self.run_command("frozen", "pass", "--phase", "confirmation", "--freeze", "v1"), 0)
        self.assertEqual(lab.load(self.root / "results/runs/frozen/run.json")["freeze_id"], "v1")

    def test_freeze_detects_added_file(self):
        self.ready_freeze()
        (self.root / "src/new.py").write_text("added=1\n")
        self.assertEqual(self.call("verify", "--id", "v1"), 2)

    def test_freeze_detects_changed_file(self):
        self.ready_freeze()
        (self.root / "src/model.py").write_text("value=42\n")
        self.assertEqual(self.call("verify", "--id", "v1"), 2)

    def test_freeze_refuses_uncommitted_source(self):
        (self.root / "docs/PROTOCOL.md").write_text("Status: READY_TO_FREEZE\n")
        self.initgit()
        (self.root / "src/model.py").write_text("value=42\n")
        self.assertEqual(self.call("freeze", "--id", "v1", "--paths", "src", "docs/PROTOCOL.md"), 2)

    def test_checkpoint_exact_file_only(self):
        self.initgit()
        (self.root / "owned.txt").write_text("ours\n")
        (self.root / "unrelated.txt").write_text("not ours\n")
        self.assertEqual(self.call("checkpoint", "--message", "test: selected file", "--paths", "owned.txt"), 0)
        committed = self.git("show", "--format=", "--name-only", "HEAD").stdout.decode().splitlines()
        self.assertEqual(committed, ["owned.txt"])
        self.assertIn("unrelated.txt", self.git("ls-files", "--others", "--exclude-standard").stdout.decode())

    def test_checkpoint_refuses_preexisting_index(self):
        self.initgit()
        (self.root / "foreign.txt").write_text("owner\n")
        (self.root / "ours.txt").write_text("agent\n")
        self.git("add", "--", "foreign.txt")
        self.assertEqual(self.call("checkpoint", "--message", "test", "--paths", "ours.txt"), 2)
        staged = self.git("diff", "--cached", "--name-only").stdout.decode().strip()
        self.assertEqual(staged, "foreign.txt")

    def test_checkpoint_refuses_directory_and_sensitive_filename(self):
        self.initgit()
        (self.root / ".env").write_text("not-a-real-secret\n")
        for path in (".", "src", ".env"):
            self.assertEqual(self.call("checkpoint", "--message", "test", "--paths", path), 2)

    def test_checkpoint_refuses_secret_content(self):
        self.initgit()
        (self.root / "oops.txt").write_text("sk-proj-" + "x"*40 + "\n")
        self.assertEqual(self.call("checkpoint", "--message", "test", "--paths", "oops.txt"), 2)

    def test_checkpoint_refuses_large_file(self):
        self.initgit()
        (self.root / "large.txt").write_text("a"*20001)
        self.assertEqual(self.call("checkpoint", "--message", "test", "--paths", "large.txt"), 2)

    def test_advisory_lock_is_exclusive(self):
        with lab.lock(self.root, "runner"):
            self.assertEqual(self.call("reconcile"), 2)

    def test_orphaned_run_reconciliation_preserves_output(self):
        path = self.root / "results/runs/orphan/run.json"
        lab.atomic(path, {"run_id": "orphan", "status": "running", "pid": None})
        (path.parent / "partial.json").write_text('{"partial":true}\n')
        self.assertEqual(self.call("reconcile"), 0)
        self.assertEqual(lab.load(path)["status"], "interrupted_unverified")
        self.assertTrue((path.parent / "partial.json").exists())

    def test_note_uses_unique_event_files(self):
        self.assertEqual(self.call("note", "--kind", "test", "--text", "first"), 0)
        self.assertEqual(self.call("note", "--kind", "test", "--text", "second"), 0)
        self.assertEqual(len(list((self.root / ".research/events").glob("*.json"))), 2)


class SanityTests(unittest.TestCase):
    def test_supplied_circle_example(self):
        from examples.circle_sanity import calculate
        output = calculate()
        self.assertFalse(output["novel_research_result"])
        self.assertEqual(output["off_ring_true"], "1/2")
        self.assertEqual(output["off_ring_alternative"], "5/4")


if __name__ == "__main__":
    unittest.main()
