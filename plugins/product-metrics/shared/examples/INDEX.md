# Учебный реестр метрик

Здесь шестнадцать вымышленных определений четырёх продуктов. Две метрики с названием MAU намеренно различаются: Monthly Active Users означает активных пользователей за месяц, но границы месяца и активность нужно уточнять.

| id | Продукт | Название | Синонимы | Версия | Статус | Формат | Определение |
|---|---|---|---|---|---|---|---|
| atlas.active_users_monthly | atlas | Активные пользователи за месяц | MAU; месячная аудитория; завершившие урок | 1 | draft | card | [Карточка](products/atlas/metrics/active_users_monthly.md) |
| beacon.active_users_monthly | beacon | Активные пользователи за месяц | MAU; месячная аудитория; активные за 30 дней | 1 | draft | card | [Карточка](products/beacon/metrics/active_users_monthly.md) |
| beacon.scenarios | beacon | Начатые сценарии | объём; frequency; попытки согласования | 1 | draft | card | [Карточка](products/beacon/metrics/scenarios.md) |
| beacon.successful_scenarios | beacon | Успешные сценарии | завершённые согласования; успешные попытки | 1 | draft | card | [Карточка](products/beacon/metrics/successful_scenarios.md) |
| beacon.success_rate | beacon | Доля успешных сценариев | success rate; доля успеха | 1 | draft | card | [Карточка](products/beacon/metrics/success_rate.md) |
| beacon.successful_scenario_time_mean | beacon | Среднее время успешного сценария | длительность; время согласования; mean duration | 1 | draft | card | [Карточка](products/beacon/metrics/successful_scenario_time_mean.md) |
| platform.wau | platform | Недельная активная аудитория | WAU; weekly active users; недельная аудитория; активные за неделю | 1 | draft | card | [Карточка](products/platform/metrics/wau.md) |
| platform.wau_retained | platform | WAU: удержанные | retained; удержанные; активные две недели подряд | 1 | draft | card | [Карточка](products/platform/metrics/wau_retained.md) |
| platform.wau_new | platform | WAU: новые | new; новые пользователи; первая активность | 1 | draft | card | [Карточка](products/platform/metrics/wau_new.md) |
| platform.wau_resurrected | platform | WAU: вернувшиеся | resurrected; вернувшиеся; возвращённые | 1 | draft | card | [Карточка](products/platform/metrics/wau_resurrected.md) |
| platform.reminders_sent | platform | Отправленные напоминания | напоминания; reminders; рассылка напоминаний | 1 | draft | card | [Карточка](products/platform/metrics/reminders_sent.md) |
| platform.reminder_unsubscribes | platform | Отписки от напоминаний | unsubscribes; отписки; отключили напоминания | 1 | draft | card | [Карточка](products/platform/metrics/reminder_unsubscribes.md) |
| shop.orders | shop | Оплаченные заказы | orders; заказы; число заказов | 1 | draft | card | [Карточка](products/shop/metrics/orders.md) |
| shop.revenue | shop | Выручка с оплаченных заказов | revenue; выручка; оборот | 1 | draft | card | [Карточка](products/shop/metrics/revenue.md) |
| shop.aov | shop | Средний чек | AOV; average order value; средний чек; avg order value | 1 | draft | card | [Карточка](products/shop/metrics/aov.md) |
| shop.order_segment | shop | Сегмент заказа | сегмент; order segment; сегмент заказа | 1 | draft | card | [Карточка](products/shop/metrics/order_segment.md) |

Карточки Beacon связаны в [системе метрик](products/beacon/METRICS_SYSTEM.md). Условия учёта событий находятся в [учебных правилах](DATA_CONTRACT.md); они не подтверждены реальными данными. Карточки Platform связаны в [системе метрик](products/platform/METRICS_SYSTEM.md), карточки Shop - в [системе метрик](products/shop/METRICS_SYSTEM.md). Учебные ряды лежат в папке [data](data/): [aov-weekly.csv](data/aov-weekly.csv), [aov-segments.csv](data/aov-segments.csv), [wau-partition.csv](data/wau-partition.csv). Пустая ячейка в них означает неизвестное значение. В [wau-partition.csv](data/wau-partition.csv) значения WAU в строках t2 и t3 (5.5 и 5.75) модельные (в файле помечены в колонке `note`), из учебной рекурренции `WAU(t+1) = WAU(t)/2 + 3`, а не наблюдённые.
