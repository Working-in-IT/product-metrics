# Учебный реестр метрик

Здесь шесть вымышленных определений двух продуктов. Две метрики с названием MAU намеренно различаются: Monthly Active Users означает активных пользователей за месяц, но границы месяца и активность нужно уточнять.

| id | Продукт | Название | Синонимы | Версия | Статус | Формат | Определение |
|---|---|---|---|---|---|---|---|
| atlas.active_users_monthly | atlas | Активные пользователи за месяц | MAU; месячная аудитория; завершившие урок | 1 | draft | card | [Карточка](products/atlas/metrics/active_users_monthly.md) |
| beacon.active_users_monthly | beacon | Активные пользователи за месяц | MAU; месячная аудитория; активные за 30 дней | 1 | draft | card | [Карточка](products/beacon/metrics/active_users_monthly.md) |
| beacon.scenarios | beacon | Начатые сценарии | объём; frequency; попытки согласования | 1 | draft | card | [Карточка](products/beacon/metrics/scenarios.md) |
| beacon.successful_scenarios | beacon | Успешные сценарии | завершённые согласования; успешные попытки | 1 | draft | card | [Карточка](products/beacon/metrics/successful_scenarios.md) |
| beacon.success_rate | beacon | Доля успешных сценариев | success rate; доля успеха | 1 | draft | card | [Карточка](products/beacon/metrics/success_rate.md) |
| beacon.successful_scenario_time_mean | beacon | Среднее время успешного сценария | длительность; время согласования; mean duration | 1 | draft | card | [Карточка](products/beacon/metrics/successful_scenario_time_mean.md) |

Карточки Beacon связаны в [системе метрик](products/beacon/METRICS_SYSTEM.md). Условия учёта событий находятся в [учебных правилах](DATA_CONTRACT.md); они не подтверждены реальными данными.
