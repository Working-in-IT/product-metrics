import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "plugins/product-metrics/scripts/render_system.py"


def system(second_version):
    goals, relations = [], []
    for goal, version, source, target in [
        ("old", 1, "billing.eur", "billing.usd"),
        ("new", second_version, "billing.usd", "billing.eur"),
    ]:
        goals.append({"id": goal, "scope": "billing", "statement": goal, "metrics": [
            {"metric_id": key, "definition_version": version, "role": role, "rationale": "FX"}
            for key, role in [(source, "primary"), (target, "driver")]
        ]})
        relations.append({"goal_id": goal, "type": "calculated_from", "from": source, "to": target,
                          "status": "defined", "basis": f"{source} = {target} × FX", "evidence": ["rates"]})
    return {"schema_version": 1, "system_id": "billing", "product_ids": ["billing"],
            "status": "draft", "goals": goals, "relations": relations}


class RenderSystemTest(unittest.TestCase):
    def render(self, header, *extra_args):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "system.md"
            path.write_text(f"---\n{header}\n---\n", encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), str(path), *extra_args],
                                  text=True, capture_output=True)

    def test_different_versions_render_together(self):
        result = self.render(yaml.safe_dump(system(2)))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("==>"), 2)

    def test_same_version_cycle_across_goals_is_rejected(self):
        result = self.render(yaml.safe_dump(system(1)))
        self.assertEqual(result.returncode, 1)
        self.assertIn("цикл", result.stderr)
        self.assertEqual(result.stdout, "")

    def test_duplicate_key_never_renders(self):
        header = yaml.safe_dump(system(2))
        for key, duplicate in [
            ("relations", header + "relations: []"),
            ("id", header.replace("- id: old\n", "- id: ignored\n  id: old\n", 1)),
        ]:
            with self.subTest(key=key):
                result = self.render(duplicate, "--force")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"Duplicate YAML key: {key}", result.stderr)
                self.assertEqual(result.stdout, "")

    def test_yaml_merge_allows_explicit_override(self):
        header = yaml.safe_dump(system(2))
        header = header.replace("status: draft", "<<: &defaults {status: agreed}\nstatus: draft")
        result = self.render(header)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
