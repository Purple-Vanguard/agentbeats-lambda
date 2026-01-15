#!/usr/bin/env python3
"""Run the LegalEagleEye scenario and export attack_succeeded.json evidence."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

SCENARIO_ID = "legaleagleeye"
TEAM_NAME = "purple_vanguard"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    scenario_dir = (
        repo_root
        / "scenarios"
        / "security_arena"
        / "submissions"
        / TEAM_NAME
        / SCENARIO_ID
    )
    scenario_toml = scenario_dir / f"scenario_{SCENARIO_ID}.toml"
    results_dir = scenario_dir / "test_results"
    results_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["AGENTBEATS_RESULTS_DIR"] = str(results_dir)

    cmd = [
        "uv",
        "run",
        "agentbeats-run",
        str(scenario_toml),
    ]

    print(f"Running scenario: {' '.join(cmd)}")
    completed = subprocess.run(cmd, env=env, check=False)
    if completed.returncode != 0:
        raise SystemExit(f"Scenario run failed with exit code {completed.returncode}")

    attack_path = results_dir / "attack_succeeded.json"
    if not attack_path.exists():
        raise SystemExit(f"Missing attack evidence at {attack_path}")

    attack_data = json.loads(attack_path.read_text())
    if not attack_data.get("succeeded"):
        raise SystemExit("Attack did not succeed; re-run or adjust scenario.")

    output_path = scenario_dir / "attack_succeeded.json"
    shutil.copyfile(attack_path, output_path)

    print(f"Exported attack evidence to {output_path}")


if __name__ == "__main__":
    main()
