---
schema_version: 1
system_id: platform.weekly_audience
product_ids: [platform]
status: draft
owner: null
last_reviewed_at: "2026-10-04"
goals:
  - id: weekly_audience
    statement: "Видеть, из каких групп складывается недельная полезная аудитория, и проверить гипотезу о напоминаниях"
    scope: "Внутренняя платформа Platform; событие task_completed; учебная система"
    metrics:
      - metric_id: platform.wau
        definition_version: 1
        role: primary
        rationale: "Недельная аудитория с полезным действием"
      - metric_id: platform.wau_retained
        definition_version: 1
        role: diagnostic
        rationale: "Активные на этой и прошлой неделе"
      - metric_id: platform.wau_new
        definition_version: 1
        role: diagnostic
        rationale: "Первая активность на этой неделе"
      - metric_id: platform.wau_resurrected
        definition_version: 1
        role: diagnostic
        rationale: "Вернулись после паузы"
      - metric_id: platform.reminders_sent
        definition_version: 1
        role: driver
        rationale: "Кандидат в рычаги; гипотеза, не доказано"
      - metric_id: platform.reminder_unsubscribes
        definition_version: 1
        role: guardrail
        rationale: "Противовес усталости от напоминаний"
relations:
  - type: calculated_from
    from: platform.wau
    to: platform.wau_retained
    goal_id: weekly_audience
    basis: "wau = retained + new + resurrected; одна неделя, одно событие, один набор идентификаторов; части не пересекаются и покрывают аудиторию при P входит в H и полной истории H. WAU не равна сумме DAU"
    evidence: ["metrics/wau.md", "../../data/wau-partition.csv"]
    status: defined
  - type: calculated_from
    from: platform.wau
    to: platform.wau_new
    goal_id: weekly_audience
    basis: "wau = retained + new + resurrected; те же правила совместимости; new зависит от полноты истории"
    evidence: ["metrics/wau.md"]
    status: defined
  - type: calculated_from
    from: platform.wau
    to: platform.wau_resurrected
    goal_id: weekly_audience
    basis: "wau = retained + new + resurrected; те же правила совместимости; сегмент пауз определённой длины не заменяет эту часть"
    evidence: ["metrics/wau.md"]
    status: defined
  - type: guarded_by
    from: platform.reminders_sent
    to: platform.reminder_unsubscribes
    goal_id: weekly_audience
    basis: "Рост напоминаний оценивать вместе с отписками: риск усталости; порог не задан и требует согласования"
    evidence: []
    status: proposed
  - type: hypothesized_driver
    from: platform.reminders_sent
    to: platform.wau_retained
    goal_id: weekly_audience
    basis: "Напоминание может повысить вероятность повторной активности на следующей неделе; механизм не проверен, альтернативы (сезонность, изменения продукта) не исключены; ступень: нет | коррелирует: неизвестно | величина: неизвестно | лаг: неизвестно | область: неизвестно"
    evidence: []
    status: untested
---

# Система метрик Platform

Вымышленная система показывает, как отделить состав аудитории от рычагов влияния. Все решения здесь - учебные предложения.

## Цель и решение

Понять состав недельной аудитории и решить, какую гипотезу проверять первой. Система не доказывает, что напоминания увеличивают возврат.

## Роли метрик

Основная - [WAU](metrics/wau.md). Состав: [удержанные](metrics/wau_retained.md), [новые](metrics/wau_new.md), [вернувшиеся](metrics/wau_resurrected.md). Рычаг-кандидат - [напоминания](metrics/reminders_sent.md), противовес - [отписки](metrics/reminder_unsubscribes.md).

## Связи и основания

Три связи `calculated_from` - формула состава, не управление. Прошлая аудитория - историческая база, ею нельзя управлять сейчас. Проверка на неделе t1 ([данные](../../data/wau-partition.csv)): `2 + 2 + 1 = 5`. Гипотеза о напоминаниях - `untested`; формула её не подтверждает.

## Пробелы и следующая проверка

Неизвестны: реальное событие активности, полнота истории, учёт анонимов, существование напоминаний, порог отписок, исходные уровни. Следующий шаг - проверить полноту истории на реальных данных, затем сравнить удержание у получивших и не получивших напоминание при совместимых окнах.
