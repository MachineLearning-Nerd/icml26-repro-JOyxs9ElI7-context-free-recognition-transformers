"""Portability checks for the evaluator-visible candidate auditor."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from audit_candidate import resolve_candidate_root  # noqa: E402


class CandidateAuditPortabilityTests(unittest.TestCase):
    def test_repository_layout_selects_nested_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script = root / "repro" / "src" / "audit_candidate.py"
            script.parent.mkdir(parents=True)
            (root / "candidate_space").mkdir()
            self.assertEqual(resolve_candidate_root(script), (root / "candidate_space").resolve())

    def test_space_layout_selects_download_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            script = root / "evidence" / "code" / "audit_candidate.py"
            script.parent.mkdir(parents=True)
            self.assertEqual(resolve_candidate_root(script), root.resolve())


if __name__ == "__main__":
    unittest.main()
