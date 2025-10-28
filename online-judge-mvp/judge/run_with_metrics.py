#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
import resource


def parse_args():
    parser = argparse.ArgumentParser(description="Run command with precise timing and memory metrics.")
    parser.add_argument("--cmd", nargs="+", required=True, help="Command to execute")
    parser.add_argument("--stdin", required=True, help="Input file path")
    parser.add_argument("--stdout", required=True, help="Output file path")
    parser.add_argument("--stderr", required=True, help="Stderr file path")
    parser.add_argument("--metrics", required=True, help="Metrics JSON output path")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(os.path.dirname(args.metrics) or ".", exist_ok=True)

    with open(args.stdin, "rb") as fin, \
            open(args.stdout, "wb") as fout, \
            open(args.stderr, "wb") as ferr:
        start = time.perf_counter()
        completed = subprocess.run(args.cmd, stdin=fin, stdout=fout, stderr=ferr)
        end = time.perf_counter()

    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    metrics = {
        "elapsed_seconds": end - start,
        "max_rss_kb": getattr(usage, "ru_maxrss", None),
        "exit_code": completed.returncode
    }
    with open(args.metrics, "w", encoding="utf-8") as handle:
        json.dump(metrics, handle)

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
