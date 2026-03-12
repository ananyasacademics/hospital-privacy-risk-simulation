"""
Reproducibility utilities for Hospital Privacy Risk Simulation.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict


def generate_run_id() -> str:
    """Generate timestamp-based run ID."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def compute_file_hash(file_path: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def write_run_manifest(manifest: Dict, output_path: str) -> None:
    """Write manifest JSON describing the run."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def write_execution_log(log_lines: list[str], output_path: str) -> None:
    """Write execution log text file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for line in log_lines:
            f.write(line + "\n")


def write_judge_summary(summary_text: str, output_path: str) -> None:
    """Write a simple judge-friendly summary."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary_text)