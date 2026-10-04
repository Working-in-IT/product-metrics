#!/usr/bin/env python3
"""Check plugin packaging and synthetic examples. Does not modify files."""
import json
import re
import sys
from pathlib import Path

import yaml

EXPECTED_SKILLS = {"metrics-setup", "metric-catalog", "metrics-system", "metrics-review", "diagnose-metric", "metrics-memo"}
EXPECTED_PRODUCTS = {"atlas", "beacon", "shop", "platform"}
EXPECTED_CARDS = 16
AMBIGUOUS_ALIAS = ("MAU", 2)
SKILL_BODY_MAX_WORDS = 400
SKILL_DESCRIPTION_MAX_CHARS = 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys, including metadata that would otherwise be lost."""


def mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        require(key not in result, f"Duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    require(match, f"Unclosed YAML: {path}")
    result = yaml.load(match[1], Loader=UniqueLoader)
    require(isinstance(result, dict), f"Metadata must be an object: {path}")
    return result


def validate(root):
    root = root.resolve()
    plugin = root / "plugins/product-metrics"
    shared = plugin / "shared"
    manifests = [json.loads((plugin / p).read_text(encoding="utf-8")) for p in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json")]
    for manifest in manifests:
        for key in ("name", "version", "license", "repository"):
            require(manifest[key] == manifests[0][key], f"Manifest mismatch: {key}")
    require(manifests[0]["name"] == "product-metrics", "Plugin name")
    for file, kind in ((".agents/plugins/marketplace.json", "codex"), (".claude-plugin/marketplace.json", "claude")):
        market = json.loads((root / file).read_text(encoding="utf-8"))
        require(market["name"] == "working-in-it-metrics" and len(market["plugins"]) == 1, "Marketplace identity")
        entry = market["plugins"][0]
        source = entry["source"]["path"] if kind == "codex" else entry["source"]
        require(entry["name"] == "product-metrics" and (root / source).resolve() == plugin, "Marketplace source")
        if kind == "claude":
            require(entry["version"] == manifests[0]["version"], "Marketplace version")

    skills = list((plugin / "skills").glob("*/SKILL.md"))
    found_skills = {p.parent.name for p in skills}
    require(found_skills == EXPECTED_SKILLS, f"Skill set differs: missing {sorted(EXPECTED_SKILLS - found_skills)}, extra {sorted(found_skills - EXPECTED_SKILLS)}")
    for path in skills:
        meta = frontmatter(path)
        require(meta["name"] == path.parent.name and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["name"]), f"Skill name: {path}")
        description = meta["description"]
        require(isinstance(description, str) and 0 < len(description) <= SKILL_DESCRIPTION_MAX_CHARS, f"Skill description: {path}")
        require(re.search(r"[А-Яа-яЁё]", description) and re.search(r"[A-Za-z]{4}", description), f"Description needs Russian and English sentences: {path}")
        body = re.sub(r"\A---\n.*?\n---\n", "", path.read_text(encoding="utf-8"), count=1, flags=re.S)
        require(len(body.split()) <= SKILL_BODY_MAX_WORDS, f"Skill body over {SKILL_BODY_MAX_WORDS} words: {path}")

    required = {"schema_version", "id", "name", "product_id", "aliases", "definition_version", "status", "owner", "unit", "effective_from", "last_reviewed_at"}
    cards = {}
    for path in sorted((shared / "examples/products").glob("*/metrics/*.md")):
        meta = frontmatter(path)
        require(required <= meta.keys(), f"Missing fields: {path}")
        require(type(meta["schema_version"]) is int and meta["schema_version"] == 1, "Schema version")
        require(type(meta["definition_version"]) is int and meta["definition_version"] > 0, "Definition version")
        require(re.fullmatch(r"[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*", meta["id"]), "Metric ID")
        require(meta["id"].split(".")[0] == meta["product_id"] and meta["id"] not in cards, "Product or duplicate ID")
        require(meta["status"] in {"draft", "agreed", "deprecated"}, "Metric status")
        require(meta["unit"] in {"count", "ratio", "percent", "seconds", "minutes", "hours", "score", "currency", "other"}, "Metric unit")
        require(isinstance(meta["name"], str) and meta["name"].strip(), "Metric name")
        require(meta["owner"] is None or isinstance(meta["owner"], str), "Metric owner")
        require(isinstance(meta["aliases"], list) and all(isinstance(a, str) for a in meta["aliases"]), "Aliases")
        for field in ("effective_from", "last_reviewed_at"):
            require(meta[field] is None or (isinstance(meta[field], str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta[field])), f"Quote date: {field}")
        cards[meta["id"]] = (path, meta)
    require(len(cards) == EXPECTED_CARDS, f"Expected {EXPECTED_CARDS} synthetic cards, found {len(cards)}")
    require({m["product_id"] for _, m in cards.values()} == EXPECTED_PRODUCTS, "Synthetic products differ from expected set")
    index = shared / "examples/INDEX.md"
    rows = []
    for line in index.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] not in cards:
            require(cells[0] == "id", f"Unknown index ID: {cells[0]}")
            continue
        path, meta = cards[cells[0]]
        expected = [meta["product_id"], meta["name"], "; ".join(meta["aliases"]), str(meta["definition_version"]), meta["status"], "card"]
        require(cells[1:7] == expected, f"Index differs: {meta['id']}")
        link = re.search(r"\]\(([^)]+)\)", cells[7])
        require(link and (index.parent / link[1]).resolve() == path, "Index link")
        rows.append(meta["id"])
    require(len(rows) == len(set(rows)) == len(cards), "Index coverage")
    alias, count = AMBIGUOUS_ALIAS
    require(sum(alias in m["aliases"] for _, m in cards.values()) == count, "Ambiguous alias fixture")

    links = 0
    for path in root.rglob("*"):
        if {".git", ".venv", "__pycache__"}.intersection(path.relative_to(root).parts):
            continue
        require(not path.is_symlink(), f"Symlink: {path}")
        if not path.is_file() or path.suffix != ".md":
            continue
        body = re.sub(r"(?ms)^```.*?^```[^\n]*", "", path.read_text(encoding="utf-8"))
        refs = re.findall(r"\]\(([^)]+)\)", body)
        for rel in frontmatter(path).get("relations", []):
            refs.extend(rel["evidence"])
        for ref in refs:
            if ref.startswith(("https://", "http://", "#")):
                continue
            dest = (path.parent / ref.split("#")[0]).resolve()
            require(dest.is_relative_to(root) and dest.exists(), f"Broken/local external link: {path.relative_to(root)} -> {ref}")
            if path.is_relative_to(plugin):
                require(dest.is_relative_to(plugin), f"Installed plugin needs repo-only file: {path}")
            links += 1

    relations = 0
    for path in (shared / "examples/products").glob("*/METRICS_SYSTEM.md"):
        system = frontmatter(path)
        goals = {g["id"]: g for g in system["goals"]}
        require(len(goals) == len(system["goals"]), "Duplicate goal")
        for goal in goals.values():
            seen = set()
            for metric in goal["metrics"]:
                mid = metric["metric_id"]
                require(mid in cards and mid not in seen, "Missing/duplicate goal metric")
                seen.add(mid)
                require(metric["definition_version"] == cards[mid][1]["definition_version"], f"Stale consumer: {mid}")
                require(metric["role"] in {"primary", "driver", "guardrail", "diagnostic"}, "Metric role")
        statuses = {"calculated_from": {"defined"}, "guarded_by": {"proposed", "agreed"}, "hypothesized_driver": {"untested", "supported", "rejected"}}
        edges = {}
        for rel in system["relations"]:
            require(rel["goal_id"] in goals, "Unknown relation goal")
            members = {m["metric_id"] for m in goals[rel["goal_id"]]["metrics"]}
            require({rel["from"], rel["to"]} <= members, "Relation scope")
            require(rel["type"] in statuses and rel["status"] in statuses[rel["type"]], "Relation status")
            require(rel["basis"] and isinstance(rel["evidence"], list), "Relation basis")
            if rel["status"] in {"defined", "agreed", "supported", "rejected"}:
                require(rel["evidence"], "Missing evidence")
            if rel["type"] == "calculated_from":
                edges.setdefault(rel["from"], []).append(rel["to"])
            relations += 1
        def visit(key, trail):
            require(key not in trail, "Calculation cycle")
            for nxt in edges.get(key, []):
                visit(nxt, trail + [key])
        for key in edges:
            visit(key, [])
    return {"status": "passed", "version": manifests[0]["version"], "skills": len(skills), "example_cards": len(cards), "relations": relations, "local_links": links}


if __name__ == "__main__":
    try:
        package = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
        print(json.dumps(validate(package), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, yaml.YAMLError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        sys.exit(1)
