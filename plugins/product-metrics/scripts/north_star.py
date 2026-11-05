"""Check a proposed North Star identity and attribute its change. Python standard library only."""

import argparse
import csv
import json
import math
import sys
from contextlib import nullcontext
from datetime import date
from fractions import Fraction


def read_periods(stream):
    reader = csv.reader(stream, strict=True)
    header = [name.strip() for name in next(reader, [])]
    if header[:2] != ["period", "nsm"] or len(header) < 3:
        raise ValueError("Expected header: period,nsm,<factor>,...")
    if "" in header or len(set(header)) != len(header):
        raise ValueError("Each column needs a distinct, nonempty name")

    periods = []
    for row in reader:
        if len(row) != len(header):
            raise ValueError(f"Line {reader.line_num}: expected {len(header)} columns")
        period = row[0].strip()
        if date.fromisoformat(period).isoformat() != period:
            raise ValueError(f"Line {reader.line_num}: expected YYYY-MM-DD")
        if periods and period <= periods[-1][0]:
            raise ValueError(f"Line {reader.line_num}: periods must be in increasing order")
        try:
            total, *factors = [Fraction(value.strip()) for value in row[1:]]
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"Line {reader.line_num}: expected a finite number or fraction") from exc
        periods.append((period, total, factors))
    if not periods:
        raise ValueError("Provide at least one period")
    return header[2:], periods


def check_tree(names, periods, combine):
    mismatches = []
    for period, total, factors in periods:
        calculated = combine(factors)
        if calculated != total:
            mismatches.append({"period": period, "observed": str(total), "calculated": str(calculated)})
    if mismatches:
        return {"reconciles": False, "mismatches": mismatches}

    result = {"reconciles": True, "periods": len(periods)}
    nonzero_totals = {total for _, total, _ in periods if total}
    if len(nonzero_totals) < 2:
        result["proportionality"] = "insufficient variation"
    else:
        # A fixed ratio is a prompt to inspect the definitions. It can occur by chance.
        _, base_total, base = next(row for row in periods if row[1])
        result["check_definitions"] = [
            name for i, name in enumerate(names)
            if base[i] and all(factors[i] * base_total == base[i] * total for _, total, factors in periods)
        ]

    if len(periods) > 1:
        start, before, first = periods[0]
        end, after, last = periods[-1]
        current = first.copy()
        previous = before
        contributions = []
        for i, name in enumerate(names):
            current[i] = last[i]
            updated = combine(current)
            contributions.append({"factor": name, "change": str(updated - previous)})
            previous = updated
        result["change"] = {"from": start, "to": end, "delta": str(after - before),
                            "contributions_in_order": contributions}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", choices=["sum", "product"])
    parser.add_argument("csv", help="CSV file or - for standard input")
    args = parser.parse_args()
    try:
        source = nullcontext(sys.stdin) if args.csv == "-" else open(args.csv, encoding="utf-8-sig", newline="")
        with source as stream:
            names, periods = read_periods(stream)
        result = check_tree(names, periods, sum if args.formula == "sum" else math.prod)
    except (OSError, csv.Error, ValueError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["reconciles"] else 1


if __name__ == "__main__":
    sys.exit(main())
