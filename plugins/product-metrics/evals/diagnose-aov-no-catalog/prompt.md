---
name: diagnose-aov-no-catalog
tags: [diagnose, no-catalog]
runs: 2
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Средний чек в магазине Shop упал с 67,9 до 61,7. Окна по 1000 заказов. По сегментам:
- Premium: 700 заказов со средним чеком 85 в окне A, 550 заказов со средним чеком 86 в окне B.
- Standard: 300 заказов со средним 28 в окне A, 450 заказов со средним 32 в окне B.
Оба сегмента выросли по среднему чеку, а общий упал. Почему так и что делать?
