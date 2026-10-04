# Профиль учебного каталога

Каталог содержит только вымышленные определения. Все пути ниже относительны к этой папке.

- Реестр: [INDEX.md](INDEX.md).
- Продукты: `atlas` - учебный портал Atlas; `beacon` - сервис согласования Beacon; `shop` - учебный магазин Shop (случай среднего чека); `platform` - учебная внутренняя платформа Platform (случай недельной аудитории).
- Карточки: `products/<product_id>/metrics/<metric_name>.md`.
- Системы: `products/<product_id>/METRICS_SYSTEM.md`.
- История: `products/<product_id>/metrics/history/<metric_name>/v<N>.md`.
- Проекты изменений: `products/<product_id>/metrics/proposals/<metric_name>-v<N>.md`.
- Источник правил для Atlas и Beacon: [DATA_CONTRACT.md](DATA_CONTRACT.md). Правила Shop и Platform записаны в их карточках.
- Учебные данные Shop и Platform: `data/*.csv` ([aov-weekly.csv](data/aov-weekly.csv), [aov-segments.csv](data/aov-segments.csv), [wau-partition.csv](data/wau-partition.csv)); пустая ячейка - неизвестное значение.
- Старые спецификации отсутствуют: пример создан с нуля.
- Владельцы и согласование: отсутствуют, все карточки `draft`.
- Для пробных изменений используйте отдельную копию; журнал - `CHANGELOG.md` в этой копии, создаётся при первой записи.

Пример показывает устройство каталога и не предназначен для подключения к реальным данным.
