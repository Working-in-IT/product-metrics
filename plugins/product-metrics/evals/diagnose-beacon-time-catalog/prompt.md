---
name: diagnose-beacon-time-catalog
tags: [diagnose, catalog]
runs: 2
max_turns: 20
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

В Beacon среднее время успешного сценария упало с 50 до 30 минут, и команда радуется. Но доля успешных сценариев упала с 80% до 60%. Это улучшение или нет? Разберись по нашему каталогу метрик.
