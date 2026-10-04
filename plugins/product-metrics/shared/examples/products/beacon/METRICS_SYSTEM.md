---
schema_version: 1
system_id: beacon.faster_approvals
product_ids: [beacon]
status: draft
owner: null
last_reviewed_at: "2026-09-30"
goals:
  - id: faster_approvals
    statement: "Сократить ожидание полезного результата согласования"
    scope: "Пользовательские сценарии Beacon; учебная система"
    metrics:
      - metric_id: beacon.successful_scenario_time_mean
        definition_version: 1
        role: primary
        rationale: "Длительность успешного пути"
      - metric_id: beacon.success_rate
        definition_version: 1
        role: guardrail
        rationale: "Не принимать рост неуспехов за ускорение"
      - metric_id: beacon.scenarios
        definition_version: 1
        role: guardrail
        rationale: "Контролировать объём и состав попыток"
      - metric_id: beacon.successful_scenarios
        definition_version: 1
        role: diagnostic
        rationale: "Числитель доли и вес среднего"
      - metric_id: beacon.active_users_monthly
        definition_version: 1
        role: diagnostic
        rationale: "Наблюдать аудиторию сервиса"
relations:
  - type: calculated_from
    from: beacon.success_rate
    to: beacon.successful_scenarios
    goal_id: faster_approvals
    basis: "success_rate = successful_scenarios / scenarios; одинаковая зрелая когорта, срез и дата получения"
    evidence: ["metrics/success_rate.md"]
    status: defined
  - type: calculated_from
    from: beacon.success_rate
    to: beacon.scenarios
    goal_id: faster_approvals
    basis: "success_rate = successful_scenarios / scenarios; одинаковая зрелая когорта, срез и дата получения"
    evidence: ["metrics/success_rate.md"]
    status: defined
  - type: calculated_from
    from: beacon.successful_scenario_time_mean
    to: beacon.successful_scenarios
    goal_id: faster_approvals
    basis: "mean_time = сумма длительностей успешных сценариев / successful_scenarios; одинаковая когорта; числитель пока без отдельной карточки"
    evidence: ["metrics/successful_scenario_time_mean.md"]
    status: defined
  - type: guarded_by
    from: beacon.successful_scenario_time_mean
    to: beacon.success_rate
    goal_id: faster_approvals
    basis: "Снижение времени оценивать при неухудшении доли успеха; допустимый порог требует согласования"
    evidence: []
    status: proposed
  - type: guarded_by
    from: beacon.successful_scenario_time_mean
    to: beacon.scenarios
    goal_id: faster_approvals
    basis: "Проверять объём и сложность попыток, чтобы исключение трудной работы не считалось ускорением"
    evidence: []
    status: proposed
  - type: hypothesized_driver
    from: beacon.successful_scenario_time_mean
    to: beacon.active_users_monthly
    goal_id: faster_approvals
    basis: "Меньшее ожидание может снижать отказ от повторного использования; нужны совместимые окна и проверка альтернативных объяснений; ступень: нет | коррелирует: неизвестно | величина: неизвестно | лаг: неизвестно | область: неизвестно"
    evidence: []
    status: untested
---

# Система метрик Beacon

Вымышленная система показывает, как связать цель с определениями, не приписывая математическим формулам причинный смысл. Все решения здесь — учебные предложения.

## Цель и решение

Цель — сократить ожидание результата согласования. Система должна помогать оценивать изменения сценария, учитывая успех, объём и состав работы.

## Роли метрик

Основной показатель — [среднее время](metrics/successful_scenario_time_mean.md), защитные — [доля успеха](metrics/success_rate.md) и [число попыток](metrics/scenarios.md). [Успешные сценарии](metrics/successful_scenarios.md) объясняют расчёт; [активная аудитория](metrics/active_users_monthly.md) помогает наблюдать использование. Версии и роли закреплены в шапке только для этой цели.

## Связи и основания

Доля успеха вычисляется из двух счётчиков одной выборки. Среднее время использует число успешных сценариев как знаменатель и вес; сумма длительностей ещё не выделена в отдельную карточку, поэтому граф вычислений частичный. Эти связи — формулы. Совместная оценка времени и успеха — защитное условие. Предположение об аудитории — гипотеза со статусом `untested`.

## Пробелы и следующая проверка

Числовых целей и исходных уровней нет. Метрика качества результата и разрез сложности ещё не определены; система недостаточна для утверждения о росте полезности. Для причинной проверки нужно совместить окна аудитории и сценариев на исходных данных и выбрать способ отделения эффекта скорости от других изменений. Следующий шаг — согласовать смысл успеха с владельцем и проверить логирование на небольшом разрешённом наборе данных.
