---
name: review-dashboard-beacon
tags: [review, dashboard, no-catalog]
runs: 2
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Сделай ревью дашборда Beacon. Там две карточки: «Время» (среднее время успешного сценария) - зелёная, значение 30 минут, было 50. «Успех» - 46,7%. Порогов на карточках нет, цели не подписаны. Это отчёт для решения о запуске новой версии сценария.
