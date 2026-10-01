#!/usr/bin/env python3
"""Execute the bundled SQL in memory; no network or organization data."""
import json
import sqlite3
from pathlib import Path


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def run():
    root = Path(__file__).resolve().parent
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript((root / "fixture.sql").read_text())
    queries = {name: (root / f"{name}.sql").read_text() for name in (
        "success_rate", "successful_scenario_time_mean")}
    parameters = {
        "product_id": "beacon",
        "period_start": "2026-08-01T00:00:00Z",
        "period_end": "2026-09-01T00:00:00Z",
        "as_of": "2026-09-04T00:00:00Z",
    }

    def calculate(**overrides):
        params = dict(parameters, **overrides)
        return [dict(db.execute(sql, params).fetchone()) for sql in queries.values()]

    rate, mean = calculate()
    check((rate["attempts"], rate["successes"], rate["success_rate"]) == (6, 3, 0.5),
          "Start boundary, end boundary, product filter or failed/cancelled/timeout denominator")
    check((mean["successes"], mean["duration_sum_seconds"], mean["mean_seconds"]) == (3, 97200, 32400.0),
          "Mean uses successes only, including completion next month and 24h duration")
    check(rate["calculation_status"] == mean["calculation_status"] == "calculated", "Maturity boundary")
    cases = ["monthly_cohort_and_product", "successful_time_and_next_month_completion", "maturity_boundary"]

    r, m = calculate(as_of="2026-09-03T23:59:59Z")
    check(r["success_rate"] is None and m["mean_seconds"] is None
          and r["calculation_status"] == m["calculation_status"] == "preliminary", "Immature cohort")
    cases.append("immature_cohort")

    r, m = calculate(period_start="2026-10-01T00:00:00Z", period_end="2026-11-01T00:00:00Z", as_of="2026-11-04T00:00:00Z")
    check((r["attempts"], r["successes"], r["calculation_status"], r["success_rate"]) == (0, 0, "empty_cohort", None)
          and m["successes"] == 0 and m["mean_seconds"] is None, "Empty cohort is not zero rate")
    cases.append("empty_cohort")

    r, m = calculate(period_start="2026-09-01T00:00:00Z", period_end="2026-10-01T00:00:00Z", as_of="2026-10-04T00:00:00Z")
    check(r["attempts"] == 1 and r["success_rate"] == 0.0
          and m["calculation_status"] == "no_successes" and m["mean_seconds"] is None, "Zero successes differs from no attempts")
    cases.append("no_successes")

    for row, name in [
        (("beacon", "s1", "2026-08-01T00:00:00Z", "success", 3600), "duplicate_prepared_scenario"),
        (("beacon", "invalid", "2026-08-01T00:00:00Z", "success", None), "missing_success_duration"),
        (("beacon", "invalid", "2026-08-01T00:00:00Z", "success", -1), "negative_duration"),
        (("beacon", "invalid", "2026-08-01T00:00:00Z", "success", 86401), "success_after_deadline"),
    ]:
        try:
            db.execute("INSERT INTO scenario_facts VALUES (?, ?, ?, ?, ?)", row)
        except sqlite3.IntegrityError:
            cases.append(name)
        else:
            raise AssertionError(f"Invalid prepared row accepted: {name}")
    db.close()
    return {"status": "passed", "scope": "synthetic prepared rows; raw-event preparation not tested",
            "engine": f"SQLite {sqlite3.sqlite_version}", "cases": cases,
            "parameters": parameters, "success_rate": rate, "successful_scenario_time_mean": mean}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
