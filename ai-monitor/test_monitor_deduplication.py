import json
from pathlib import Path

from monitor import AIMonitor


def test_seen_hashes_are_backfilled_from_weekly_summary(tmp_path, monkeypatch):
    """Scheduled checkouts only have weekly_summary.json committed today."""
    monkeypatch.chdir(tmp_path)
    Path("config.json").write_text(json.dumps({"search_terms": []}), encoding="utf-8")

    results_dir = Path("results")
    results_dir.mkdir()
    (results_dir / "weekly_summary.json").write_text(
        json.dumps(
            [
                {
                    "date": "2026-04-06",
                    "updates": [
                        {"title": "Old update", "hash": "already-seen"},
                        {"title": "Legacy entry without hash"},
                    ],
                },
                {
                    "date": "2026-04-13",
                    "updates": [
                        {"title": "Another old update", "hash": "also-seen"},
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )

    monitor = AIMonitor()

    assert "already-seen" in monitor.seen_hashes
    assert "also-seen" in monitor.seen_hashes


def test_seen_hashes_merge_persisted_file_and_weekly_summary(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("config.json").write_text(json.dumps({"search_terms": []}), encoding="utf-8")

    results_dir = Path("results")
    results_dir.mkdir()
    (results_dir / "seen_hashes.json").write_text(
        json.dumps(["persisted-only"]),
        encoding="utf-8",
    )
    (results_dir / "weekly_summary.json").write_text(
        json.dumps(
            [
                {
                    "date": "2026-04-13",
                    "updates": [
                        {"title": "Committed summary update", "hash": "summary-only"},
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )

    monitor = AIMonitor()

    assert monitor.seen_hashes == {"persisted-only", "summary-only"}
