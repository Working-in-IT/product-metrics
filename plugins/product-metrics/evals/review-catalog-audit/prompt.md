---
name: review-catalog-audit
tags: [review, catalog]
runs: 2
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Проверь каталог метрик по продукту Beacon: нет ли дублей, пробелов, противоречий. Только замечания, файлы не правь.
