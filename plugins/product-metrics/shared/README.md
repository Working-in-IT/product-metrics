# Общие материалы Product Metrics

Все шесть навыков используют этот единственный набор правил и шаблонов. Начало работы и установка описаны в README репозитория; после установки следуйте инструкциям выбранного навыка.

- [Формат](references/FORMAT.md): поля карточки, версии и типы связей.
- [Плейбук](references/PLAYBOOK.md): операции с определениями.
- [Как посчитать](references/CALCULATION.md): SQL, параметры, зависимости и свидетельства проверки; [запускаемые примеры](examples/sql/README.md).
- Ядро: [Принципы](references/PRINCIPLES.md) - объекты, переключатели, лестница свидетельств, шкала знания; [Рукопожатие с данными](references/DATA_HANDSHAKE.md) - приём CSV, таблицы, ответа MCP и запись свидетельства.
- Режимы `metrics-system`: [карты и деревья](references/MAPS_AND_TREES.md), [стартовые наборы](references/STARTER_SETS.md), [метрики эксперимента](references/EXPERIMENT_METRICS.md), [OKR](references/OKR.md).
- Режимы `metrics-review`: [ревью отчёта](references/DASHBOARD_REVIEW.md), [проверка vanity](references/VANITY_CHECK.md).
- Скиллы `diagnose-metric` и `metrics-memo`: [диагностика](references/DIAGNOSTICS.md), [ритм обзоров](references/REVIEW_CADENCE.md).
- [Записки-примеры](examples/memos/): [AOV](examples/memos/diagnosis-aov.md), [Beacon](examples/memos/diagnosis-beacon.md), [недельный AOV](examples/memos/weekly-aov.md).
- [Учебные ряды](examples/data/): `aov-weekly.csv`, `aov-segments.csv`, `wau-partition.csv`.
- [Скрипт карты](../scripts/README.md): `render_system.py` строит Mermaid из файла системы и проверяет структуру.
- [Профиль каталога](templates/CATALOG.md): шаблон настройки местных путей.
- [Карточка](templates/metric.md), [реестр](templates/INDEX.md), [система](templates/METRICS_SYSTEM.md): бланки.
- [Учебный каталог](examples/INDEX.md): шестнадцать вымышленных определений четырёх продуктов (Atlas, Beacon, Shop, Platform).
- [Проверки](CHECKS.md), [передача и обновления](SHARING.md), [источники](references/SOURCES.md).

Карточка хранит определение. Реестр хранит ссылку на карточку. Система метрик хранит её роль в цели и отношения с другими показателями. YAML-шапка - структурированные поля в начале Markdown-файла; версия определения меняется при изменении смысла расчёта. Защитная метрика ограничивает вывод об улучшении основного показателя. Причинная гипотеза требует отдельного подтверждения и не равна математической формуле.

Материалы организации создаются вне этой папки. Статус `agreed` означает согласование смысла, а состояние проверки реализации указывается отдельно. Учебные примеры не являются данными или утверждёнными определениями получателя.
