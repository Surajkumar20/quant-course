#!/usr/bin/env python3
"""Run the tests for one or more projects.

Usage:
    python tools/run_tests.py 01-foundations/p01-monte-carlo-probability
    python tools/run_tests.py 01-foundations/p02-matrix-library   # C++: configures + builds first
    python tools/run_tests.py --enabled                           # everything in tools/enabled_projects.txt

A project counts as Python if it has a tests/ folder with test_*.py files, and as C++
if it has a CMakeLists.txt. A project can be both.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"


def enabled_projects() -> list[str]:
    lines = (ROOT / "tools" / "enabled_projects.txt").read_text().splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]


def project_id(path: Path) -> str:
    m = re.match(r"(p\d\d)", path.name)
    if not m:
        sys.exit(f"cannot find a pNN id in {path.name}")
    return m.group(1)


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def cpp_build() -> int:
    if not (BUILD / "CMakeCache.txt").exists():
        rc = run(["cmake", "-S", ".", "-B", str(BUILD), "-DCMAKE_BUILD_TYPE=Release"])
        if rc:
            return rc
    return run(["cmake", "--build", str(BUILD), "-j"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("projects", nargs="*")
    ap.add_argument("--enabled", action="store_true", help="test everything in tools/enabled_projects.txt")
    args = ap.parse_args()

    projects = enabled_projects() if args.enabled else args.projects
    if not projects:
        print("No projects to test.")
        return 0

    built = False
    failures = []
    for p in projects:
        path = (ROOT / p).resolve()
        if not path.is_dir():
            sys.exit(f"no such project: {p}")
        ran = False
        if any((path / "tests").glob("test_*.py")):
            ran = True
            if run([sys.executable, "-m", "pytest", str(path), "-q"]):
                failures.append(f"{p} (python)")
        if (path / "CMakeLists.txt").exists():
            ran = True
            if not built:
                if cpp_build():
                    return 1
                built = True
            if run(["ctest", "--test-dir", str(BUILD), "-R", f"^{project_id(path)}_", "--output-on-failure"]):
                failures.append(f"{p} (c++)")
        if not ran:
            print(f"warning: {p} has no tests")

    print()
    if failures:
        print("FAILED:\n  " + "\n  ".join(failures))
        return 1
    print(f"All {len(projects)} project(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
