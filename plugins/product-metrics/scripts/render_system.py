#!/usr/bin/env python3
"""Проверить METRICS_SYSTEM.md и нарисовать его как Mermaid flowchart.

Только стандартная библиотека и PyYAML. Проверяет структуру и согласованность
шапки (формат v1), не арифметику формул. Выход: 0 - ошибок нет, 1 - есть ошибки
проверки, 2 - не удалось прочитать вход или нет PyYAML.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

ROLES = ("primary", "driver", "guardrail", "diagnostic")
RELATION_STATUSES: dict[str, tuple[str, ...]] = {
    "calculated_from": ("defined",),
    "guarded_by": ("proposed", "agreed"),
    "hypothesized_driver": ("untested", "supported", "rejected"),
}
EVIDENCE_REQUIRED = ("agreed", "supported", "rejected")
RELATION_FIELDS = ("type", "from", "to", "goal_id", "basis", "evidence", "status")
KEY_RE = re.compile(r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
STEP_5_6_RE = re.compile(r"ступень:\s*[56]\b")

EDGE_STYLE = {
    "calculated_from": ("==>", "считается из", "#2b6cb0"),
    "guarded_by": ("-.->", "guardrail", "#6b46c1"),
    "hypothesized_driver": ("-.->", "гипотеза", None),
}
HYPOTHESIS_COLORS = {"untested": "#b7791f", "supported": "#2f855a", "rejected": "#c53030"}
ROLE_CLASSES = {
    "primary": "fill:#e6f0ff,stroke:#2b6cb0,stroke-width:2px",
    "driver": "fill:#fff7e0,stroke:#b7791f",
    "guardrail": "fill:#f1e8ff,stroke:#6b46c1",
    "diagnostic": "fill:#eeeeee,stroke:#718096",
}


@dataclass(frozen=True)
class Finding:
    level: str
    where: str
    message: str

    def __str__(self) -> str:
        return f"{self.level}: {self.where}: {self.message}"


def load_header(text: str) -> tuple[dict[str, Any] | None, list[Finding]]:
    """Достать и разобрать YAML-шапку."""
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return None, [Finding("ERROR", "файл", "нет YAML-шапки между строками ---")]
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, [Finding("ERROR", "шапка", f"YAML не разобран: {exc}")]
    if not isinstance(data, dict):
        return None, [Finding("ERROR", "шапка", "шапка не является отображением")]
    return data, []


def is_positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def check_metric_entry(entry: Any, where: str, seen: set[str]) -> list[Finding]:
    if not isinstance(entry, dict):
        return [Finding("ERROR", where, "элемент metrics не является отображением")]
    findings: list[Finding] = []
    key = entry.get("metric_id")
    if not isinstance(key, str) or not KEY_RE.match(key):
        findings.append(Finding("ERROR", where, f"metric_id {key!r} не имеет вида product_id.metric_name"))
    elif key in seen:
        findings.append(Finding("ERROR", where, f"метрика {key} повторяется в цели"))
    else:
        seen.add(key)
    if not is_positive_int(entry.get("definition_version")):
        findings.append(Finding("ERROR", where, "definition_version должна быть положительным целым"))
    if entry.get("role") not in ROLES:
        findings.append(Finding("ERROR", where, f"role {entry.get('role')!r} не из {ROLES}"))
    if not entry.get("rationale"):
        findings.append(Finding("WARN", where, "пустое rationale"))
    return findings


def check_goals(goals: Any) -> tuple[list[Finding], dict[str, dict[str, str]]]:
    """Вернуть замечания и карту {goal_id: {metric_id: role}}."""
    roles_by_goal: dict[str, dict[str, str]] = {}
    if not isinstance(goals, list):
        return [Finding("ERROR", "goals", "goals должен быть списком")], roles_by_goal
    findings: list[Finding] = []
    for index, goal in enumerate(goals):
        where = f"goals[{index}]"
        if not isinstance(goal, dict):
            findings.append(Finding("ERROR", where, "цель не является отображением"))
            continue
        goal_id = goal.get("id")
        if not isinstance(goal_id, str) or not goal_id:
            findings.append(Finding("ERROR", where, "нет id цели"))
            continue
        where = f"goal {goal_id}"
        if goal_id in roles_by_goal:
            findings.append(Finding("ERROR", where, "id цели повторяется"))
        for field in ("statement", "scope"):
            if not goal.get(field):
                findings.append(Finding("WARN", where, f"пустое поле {field}"))
        metrics = goal.get("metrics")
        if not isinstance(metrics, list) or not metrics:
            findings.append(Finding("ERROR", where, "metrics должен быть непустым списком"))
            metrics = []
        seen: set[str] = set()
        for position, entry in enumerate(metrics):
            findings.extend(check_metric_entry(entry, f"{where} metrics[{position}]", seen))
        roles = {e["metric_id"]: e.get("role") for e in metrics if isinstance(e, dict) and e.get("metric_id") in seen}
        roles_by_goal[goal_id] = roles
        if roles and "primary" not in roles.values():
            findings.append(Finding("WARN", where, "нет метрики с ролью primary"))
    return findings, roles_by_goal


def check_direction(relation: dict[str, Any], roles: dict[str, str], where: str) -> list[Finding]:
    """Эвристики направления по ролям: предупреждают, не блокируют."""
    kind, src, dst = relation["type"], relation["from"], relation["to"]
    src_role, dst_role = roles.get(src), roles.get(dst)
    if kind == "guarded_by" and dst_role != "guardrail":
        return [Finding("WARN", where, f"guarded_by: {dst} не имеет роли guardrail; проверь, что `to` - страж")]
    if kind == "guarded_by" and src_role == "guardrail":
        return [Finding("WARN", where, f"guarded_by: {src} сам guardrail; возможно, направление обратное")]
    if kind == "hypothesized_driver" and src_role == "primary" and dst_role == "driver":
        return [Finding("WARN", where, "hypothesized_driver идёт от primary к driver; возможно, направление обратное")]
    return []


def check_status(relation: dict[str, Any], where: str) -> list[Finding]:
    kind, status = relation["type"], relation["status"]
    findings: list[Finding] = []
    if status not in RELATION_STATUSES[kind]:
        findings.append(Finding("ERROR", where, f"{kind}: status {status!r} не из {RELATION_STATUSES[kind]}"))
    evidence = relation["evidence"]
    if not isinstance(evidence, list):
        return findings + [Finding("ERROR", where, "evidence должен быть списком")]
    if status in EVIDENCE_REQUIRED and not evidence:
        findings.append(Finding("ERROR", where, f"status {status} требует непустой evidence"))
    if any(not isinstance(item, str) or not item.strip() for item in evidence):
        findings.append(Finding("ERROR", where, "элементы evidence должны быть непустыми строками"))
    if status == "supported" and not STEP_5_6_RE.search(str(relation["basis"])):
        findings.append(Finding("WARN", where, "supported: в basis нет строки `ступень: 5` или `ступень: 6`"))
    if kind == "calculated_from" and "=" not in str(relation["basis"]):
        findings.append(Finding("WARN", where, "calculated_from: в basis нет формулы со знаком ="))
    return findings


def check_relation(relation: Any, index: int, roles_by_goal: dict[str, dict[str, str]]) -> list[Finding]:
    where = f"relations[{index}]"
    if not isinstance(relation, dict):
        return [Finding("ERROR", where, "связь не является отображением")]
    missing = [field for field in RELATION_FIELDS if field not in relation]
    if missing:
        return [Finding("ERROR", where, f"нет полей: {', '.join(missing)}")]
    if relation["type"] not in RELATION_STATUSES:
        return [Finding("ERROR", where, f"type {relation['type']!r} не из {tuple(RELATION_STATUSES)}")]
    if not all(isinstance(relation[field], str) for field in ("from", "to", "goal_id")):
        return [Finding("ERROR", where, "from, to и goal_id должны быть строками")]
    where = f"{where} {relation['type']} {relation['from']} -> {relation['to']}"
    roles = roles_by_goal.get(relation["goal_id"])
    if roles is None:
        return [Finding("ERROR", where, f"goal_id {relation['goal_id']!r} не найден")]
    findings: list[Finding] = []
    for end in ("from", "to"):
        if relation[end] not in roles:
            findings.append(Finding("ERROR", where, f"{end}: {relation[end]!r} нет в metrics цели {relation['goal_id']}"))
    if relation["from"] == relation["to"]:
        findings.append(Finding("ERROR", where, "связь метрики с самой собой"))
    if not str(relation["basis"] or "").strip():
        findings.append(Finding("ERROR", where, "пустой basis"))
        return findings
    if findings:
        return findings
    return check_status(relation, where) + check_direction(relation, roles, where)


def find_cycles(edges: list[tuple[str, str]]) -> list[list[str]]:
    """Найти циклы в графе calculated_from поиском в глубину."""
    graph: dict[str, list[str]] = {}
    for src, dst in edges:
        graph.setdefault(src, []).append(dst)
    state: dict[str, int] = {}
    cycles: list[list[str]] = []

    def visit(node: str, path: list[str]) -> None:
        state[node] = 1
        path.append(node)
        for nxt in graph.get(node, []):
            if state.get(nxt, 0) == 1:
                cycles.append(path[path.index(nxt):] + [nxt])
            elif state.get(nxt, 0) == 0:
                visit(nxt, path)
        path.pop()
        state[node] = 2

    for start in list(graph):
        if state.get(start, 0) == 0:
            visit(start, [])
    return cycles


def check_duplicates_and_cycles(relations: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, str, str, str]] = set()
    calc_edges: list[tuple[str, str]] = []
    for index, rel in enumerate(relations):
        if not isinstance(rel, dict) or not all(f in rel for f in RELATION_FIELDS):
            continue
        triple = (str(rel["type"]), str(rel["from"]), str(rel["to"]), str(rel["goal_id"]))
        if triple in seen:
            findings.append(Finding("WARN", f"relations[{index}]", "повтор связи с тем же типом, from, to и целью"))
        seen.add(triple)
        if rel["type"] == "calculated_from":
            calc_edges.append((str(rel["from"]), str(rel["to"])))
    for cycle in find_cycles(calc_edges):
        findings.append(Finding("ERROR", "calculated_from", "цикл в расчёте: " + " -> ".join(cycle)))
    return findings


def validate(system: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if system.get("schema_version") != 1:
        findings.append(Finding("ERROR", "шапка", "schema_version должен быть 1"))
    for field in ("system_id", "product_ids", "status", "goals", "relations"):
        if field not in system:
            findings.append(Finding("ERROR", "шапка", f"нет поля {field}"))
    if system.get("status") not in ("draft", "agreed", "deprecated"):
        findings.append(Finding("ERROR", "шапка", f"status {system.get('status')!r} не из draft, agreed, deprecated"))
    goal_findings, roles_by_goal = check_goals(system.get("goals"))
    findings.extend(goal_findings)
    relations = system.get("relations")
    if not isinstance(relations, list):
        return findings + [Finding("ERROR", "relations", "relations должен быть списком")]
    for index, relation in enumerate(relations):
        findings.extend(check_relation(relation, index, roles_by_goal))
    findings.extend(check_duplicates_and_cycles(relations))
    return findings


def label(text: Any) -> str:
    return str(text).replace('"', "'").replace("\n", " ")


def render_mermaid(system: dict[str, Any]) -> str:
    """Собрать flowchart: подграф на цель, стиль ребра по типу, статус на гипотезах."""
    lines = ["flowchart LR"]
    node_ids: dict[tuple[str, str], str] = {}
    classes: dict[str, list[str]] = {role: [] for role in ROLES}
    for gi, goal in enumerate(system.get("goals") or [], start=1):
        if not isinstance(goal, dict):
            continue
        title = label(f"{goal.get('id')}: {goal.get('statement') or ''}")
        lines.append(f'  subgraph g{gi}["{title}"]')
        for mi, entry in enumerate(goal.get("metrics") or [], start=1):
            if not isinstance(entry, dict) or "metric_id" not in entry:
                continue
            node = f"g{gi}m{mi}"
            node_ids[(str(goal.get("id")), str(entry["metric_id"]))] = node
            text = label(f"{entry['metric_id']} v{entry.get('definition_version')}<br/>{entry.get('role')}")
            lines.append(f'    {node}["{text}"]')
            if entry.get("role") in classes:
                classes[entry["role"]].append(node)
        lines.append("  end")
    styles: list[str] = []
    emitted = 0
    for rel in system.get("relations") or []:
        if not isinstance(rel, dict) or rel.get("type") not in EDGE_STYLE:
            continue
        src = node_ids.get((str(rel.get("goal_id")), str(rel.get("from"))))
        dst = node_ids.get((str(rel.get("goal_id")), str(rel.get("to"))))
        if src is None or dst is None:
            continue
        arrow, caption, color = EDGE_STYLE[rel["type"]]
        if rel["type"] == "hypothesized_driver":
            caption = f"{caption}: {rel.get('status')}"
            color = HYPOTHESIS_COLORS.get(str(rel.get("status")), "#718096")
        lines.append(f'  {src} {arrow}|"{label(caption)}"| {dst}')
        styles.append(f"  linkStyle {emitted} stroke:{color},stroke-width:2px")
        emitted += 1
    for role, definition in ROLE_CLASSES.items():
        lines.append(f"  classDef {role} {definition}")
        if classes[role]:
            lines.append(f"  class {','.join(classes[role])} {role}")
    return "\n".join(lines + styles) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Проверить METRICS_SYSTEM.md и вывести Mermaid.")
    parser.add_argument("path", type=Path, help="файл METRICS_SYSTEM.md с YAML-шапкой")
    parser.add_argument("--out", type=Path, help="записать диаграмму в файл; для .md - в блоке ```mermaid")
    parser.add_argument("--force", action="store_true", help="рисовать, даже если есть ошибки проверки")
    return parser.parse_args(argv)


def emit(diagram: str, out: Path | None) -> None:
    if out is None:
        sys.stdout.write(diagram)
        return
    body = f"```mermaid\n{diagram}```\n" if out.suffix == ".md" else diagram
    out.write_text(body, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if yaml is None:
        print("Нужен PyYAML: python3 -m pip install pyyaml", file=sys.stderr)
        return 2
    try:
        text = args.path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"Не удалось прочитать {args.path}: {exc}", file=sys.stderr)
        return 2
    system, findings = load_header(text)
    if system is not None:
        findings = validate(system)
    errors = [f for f in findings if f.level == "ERROR"]
    for finding in findings:
        print(finding, file=sys.stderr)
    print(f"Итог: ошибок {len(errors)}, предупреждений {len(findings) - len(errors)}", file=sys.stderr)
    if system is not None and (not errors or args.force):
        emit(render_mermaid(system), args.out)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
