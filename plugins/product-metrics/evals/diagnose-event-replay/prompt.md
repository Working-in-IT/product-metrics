---
name: diagnose-event-replay
tags: [diagnose, review-regression, no-catalog]
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Помоги диагностировать падение доли успешных сценариев с 50% до 20%. Аналитик разделил один успех на пять строк нового журнала Beacon. Это все данные зрелой месячной когорты v1: e1 A started, e2 A completed, e3 B started, e4 B cancelled; последняя строка — повторная доставка e2 A completed. У каждой записи указан event_id, scenario_id и исход; события корректны и уложились в окно. Проверь расчёт.
