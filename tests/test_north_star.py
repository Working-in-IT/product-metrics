import json
import subprocess
import sys
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1] / "plugins/product-metrics"
SCRIPT = PLUGIN / "scripts/north_star.py"


def run_cli(formula, data):
    return subprocess.run(
        [sys.executable, str(SCRIPT), formula, "-"], input=data, text=True, capture_output=True
    )


class NorthStarTest(unittest.TestCase):
    def test_documented_example(self):
        example = PLUGIN / "shared/examples/data/north-star-orders.csv"
        output = subprocess.check_output([sys.executable, str(SCRIPT), "product", str(example)])
        result = json.loads(output)
        self.assertEqual(result["check_definitions"], [])
        self.assertEqual(result["change"]["delta"], "28")
        self.assertEqual(result["change"]["contributions_in_order"], [
            {"factor": "buyers", "change": "16"},
            {"factor": "orders_per_buyer", "change": "24"},
            {"factor": "completion_rate", "change": "-12"},
        ])

    def test_bad_middle_period_including_zero(self):
        output = run_cli("product", "period,nsm,a,b\n2026-01-01,6,3,2\n2026-02-01,0,2,2\n2026-03-01,9,3,3")
        self.assertEqual(output.returncode, 1)
        result = json.loads(output.stdout)
        self.assertEqual(result["mismatches"], [{"period": "2026-02-01", "observed": "0", "calculated": "4"}])
        self.assertNotIn("change", result)

    def test_proportional_input_needs_definition_review(self):
        output = run_cli("sum", "period,nsm,a,b\n2026-01-01,10,3,7\n2026-02-01,0,0,0\n2026-03-01,20,6,14")
        result = json.loads(output.stdout)
        self.assertEqual(result["check_definitions"], ["a", "b"])
        self.assertTrue(result["reconciles"])

    def test_offsetting_contributions_to_unchanged_root(self):
        output = run_cli("product", "period,nsm,a,b\n2026-01-01,6,2,3\n2026-02-01,6,3,2")
        result = json.loads(output.stdout)
        self.assertEqual(result["proportionality"], "insufficient variation")
        self.assertEqual(result["change"]["delta"], "0")
        self.assertEqual([c["change"] for c in result["change"]["contributions_in_order"]], ["3", "-3"])

    def test_one_period_and_fraction(self):
        output = run_cli("product", "period,nsm,a,b\n2026-01-01,1,3,1/3")
        self.assertEqual(output.returncode, 0)
        self.assertNotIn("change", json.loads(output.stdout))

    def test_malformed_input(self):
        header = "period,nsm,a\n"
        row = "2026-01-01,1,1\n"
        for data in [header, header + row + row, header + row + "2025-12-01,2,2",
                     header + "2026-01-01,1,", header + "2026-01-01,1,0/0",
                     header + "2026-01-01,NaN,1", header + "2026-01-01,1",
                     "period,nsm,a,a\n2026-01-01,1,1,1"]:
            with self.subTest(data=data):
                output = run_cli("sum", data)
                self.assertEqual(output.returncode, 2)
                self.assertIn("Invalid input", output.stderr)


if __name__ == "__main__":
    unittest.main()
