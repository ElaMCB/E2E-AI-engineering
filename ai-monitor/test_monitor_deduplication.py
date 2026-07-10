import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from monitor import AIMonitor


def test_seen_hashes_backfilled_from_weekly_summary_on_fresh_checkout(tmp_path):
    results_dir = tmp_path / "results"
    results_dir.mkdir()
    with open(results_dir / "weekly_summary.json", "w", encoding="utf-8") as f:
        json.dump(
            [
                {
                    "date": "2026-07-03",
                    "updates": [
                        {"title": "Already published", "url": "https://example.com/a", "hash": "old-hash"}
                    ],
                }
            ],
            f,
        )

    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        monitor = AIMonitor(config_path="missing-config.json")
    finally:
        os.chdir(cwd)

    assert "old-hash" in monitor.seen_hashes


def test_seen_hashes_are_saved_deterministically(tmp_path):
    cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        monitor = AIMonitor(config_path="missing-config.json")
        monitor.seen_hashes = {"b", "a"}
        monitor._save_seen_hashes()
        with open(tmp_path / "results" / "seen_hashes.json", "r", encoding="utf-8") as f:
            assert json.load(f) == ["a", "b"]
    finally:
        os.chdir(cwd)
