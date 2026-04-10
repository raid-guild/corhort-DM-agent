#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
import re


REQUIRED_FILES = [
    "state/campaign/overview.md",
    "state/campaign/current_arc.md",
    "state/campaign/world_state.md",
    "state/campaign/factions.md",
    "state/campaign/locations.md",
    "state/campaign/open_loops.md",
    "state/campaign/timeline.md",
    "state/campaign/encounter_queue.md",
    "state/handoffs/next_encounter.md",
    "state/logs/session_log.md",
    "state/logs/change_log.md",
    "state/inputs/known_characters.md",
    "state/inputs/world_seed.md",
    "state/inputs/encounter_results.md",
]


def read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def extract_section(text: str, heading: str) -> list[str]:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []
    return [line.strip() for line in match.group(1).splitlines() if line.strip().startswith("- ")]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate campaign-manager state shape.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    errors = []
    warnings = []

    for rel in REQUIRED_FILES:
        path = args.root / rel
        if not path.exists():
            errors.append(f"missing: {rel}")
            continue
        text = read(path)
        if not text.strip():
            errors.append(f"empty: {rel}")
        if "Status: scaffold" in text or "Uninitialized" in text:
            warnings.append(f"needs bootstrap: {rel}")

    queue_text = read(args.root / "state/campaign/encounter_queue.md")
    handoff_text = read(args.root / "state/handoffs/next_encounter.md")
    open_loops_text = read(args.root / "state/campaign/open_loops.md")
    session_log_text = read(args.root / "state/logs/session_log.md")

    touchpoint_ids = re.findall(r"^## (TP-\d+)\b", queue_text, flags=re.MULTILINE)
    if not touchpoint_ids:
        errors.append("encounter queue has no touchpoints")

    selected = re.search(r"^- Selected Touchpoint ID: (TP-\d+)\b", handoff_text, flags=re.MULTILINE)
    if not selected:
        errors.append("next encounter handoff is missing Selected Touchpoint ID")
    elif touchpoint_ids and selected.group(1) not in touchpoint_ids:
        errors.append(
            f"handoff references {selected.group(1)} but encounter queue contains {', '.join(touchpoint_ids)}"
        )

    arc_id = re.search(r"^- Arc ID: (ARC-\d+)\b", read(args.root / "state/campaign/current_arc.md"), flags=re.MULTILINE)
    handoff_arc = re.search(r"^- Arc ID: (ARC-\d+)\b", handoff_text, flags=re.MULTILINE)
    if arc_id and handoff_arc and arc_id.group(1) != handoff_arc.group(1):
        errors.append(f"handoff arc {handoff_arc.group(1)} does not match current arc {arc_id.group(1)}")

    active_loop_lines = extract_section(open_loops_text, "Active")
    if any(line.startswith("- [resolved] ") for line in active_loop_lines):
        errors.append("open_loops has resolved entries in the Active section")

    session_ids = re.findall(r"^## (SESSION-\d+)\b", session_log_text, flags=re.MULTILINE)
    duplicate_session_ids = sorted({session_id for session_id in session_ids if session_ids.count(session_id) > 1})
    for session_id in duplicate_session_ids:
        errors.append(f"session_log contains duplicate session heading: {session_id}")

    print("Validation report")
    print(f"- Root: {args.root}")
    print(f"- Required files checked: {len(REQUIRED_FILES)}")
    print(f"- Touchpoints found: {len(touchpoint_ids)}")
    if warnings:
        print("- Warnings:")
        for item in warnings:
            print(f"  - {item}")
    if errors:
        print("- Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("- Status: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
