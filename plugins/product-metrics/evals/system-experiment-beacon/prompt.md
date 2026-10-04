---
name: system-experiment-beacon
tags: [system, experiment, catalog]
runs: 2
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Мы запускаем A/B-тест ускорения сценария в Beacon: хотим снизить время успешного сценария. Какие метрики взять и какие допуски зафиксировать до запуска? Каталог метрик у нас в проекте.
