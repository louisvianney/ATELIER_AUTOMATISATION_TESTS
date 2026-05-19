from tester.tests import run_all

def execute_run():
    tests = run_all()
    latencies = [t["latency_ms"] for t in tests if t["latency_ms"] is not None]
    passed = sum(1 for t in tests if t["status"] == "PASS")
    failed = len(tests) - passed
    avg = round(sum(latencies) / len(latencies)) if latencies else None
    p95 = sorted(latencies)[int(len(latencies) * 0.95) - 1] if len(latencies) > 1 else (latencies[0] if latencies else None)
    return {
        "api": "Agify",
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": round(failed / len(tests), 3) if tests else 0,
            "latency_ms_avg": avg,
            "latency_ms_p95": p95
        },
        "tests": tests
    }