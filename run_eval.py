"""Run candidate solutions against each task's hidden tests.

Usage:
    python run_eval.py --reference                 # sanity check: reference solutions must pass 100%
    python run_eval.py responses/<model_name>      # evaluate a model's answers

A responses folder contains one file per task, named after the task folder,
e.g. responses/my_model/001_brazilian_plate.py
"""
import argparse
import csv
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "tasks"
RESULTS_CSV = ROOT / "results.csv"
TIMEOUT_SECONDS = 60


def run_task(task_dir: Path, candidate: Path) -> dict:
    """Copy candidate + hidden tests into an isolated temp dir and run pytest."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        shutil.copy(candidate, tmp_path / "solution.py")
        shutil.copy(task_dir / "test_hidden.py", tmp_path / "test_hidden.py")
        report = tmp_path / "report.xml"

        start = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 f"--junitxml={report}", "test_hidden.py"],
                cwd=tmp_path, capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return {"tests_passed": 0, "tests_total": 0, "passed": False,
                    "seconds": TIMEOUT_SECONDS, "error": "timeout"}
        seconds = round(time.perf_counter() - start, 2)

        if not report.exists():
            last_line = (proc.stdout.strip().splitlines() or ["no output"])[-1]
            return {"tests_passed": 0, "tests_total": 0, "passed": False,
                    "seconds": seconds, "error": last_line[:200]}

        suite = ET.parse(report).getroot()
        suite = suite if suite.tag == "testsuite" else suite.find("testsuite")
        total = int(suite.get("tests", 0))
        failed = int(suite.get("failures", 0)) + int(suite.get("errors", 0))
        first_failure = ""
        for case in suite.iter("testcase"):
            bad = case.find("failure")
            if bad is None:
                bad = case.find("error")
            if bad is not None:
                message = ((bad.get("message") or "").strip().splitlines() or [""])[0]
                first_failure = f"{case.get('name')}: {message}"[:200]
                break

        return {"tests_passed": total - failed, "tests_total": total,
                "passed": total > 0 and failed == 0, "seconds": seconds,
                "error": first_failure}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("responses", nargs="?", help="folder with one <task_id>.py per task")
    parser.add_argument("--reference", action="store_true", help="evaluate the reference solutions")
    args = parser.parse_args()
    if not args.reference and not args.responses:
        parser.error("give a responses folder or --reference")

    model = "reference" if args.reference else Path(args.responses).name
    rows = []
    for task_dir in sorted(p for p in TASKS_DIR.iterdir() if p.is_dir()):
        task_id = task_dir.name
        candidate = (task_dir / "reference.py") if args.reference else Path(args.responses) / f"{task_id}.py"
        if not candidate.exists():
            result = {"tests_passed": 0, "tests_total": 0, "passed": False,
                      "seconds": 0, "error": "missing answer file"}
        else:
            result = run_task(task_dir, candidate)
        rows.append({"timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                     "task_id": task_id, "model": model, **result})
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {task_id}: {result['tests_passed']}/{result['tests_total']} tests"
              + (f"  -> {result['error']}" if result["error"] else ""))

    solved = sum(r["passed"] for r in rows)
    print(f"\n{model}: pass@1 = {solved}/{len(rows)} tasks ({solved / len(rows):.0%})")

    new_file = not RESULTS_CSV.exists()
    with RESULTS_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new_file:
            writer.writeheader()
        writer.writerows(rows)

    # A reference solution that fails means the task itself is broken.
    if args.reference and solved < len(rows):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
