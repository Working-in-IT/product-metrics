# Eval-набор Product Metrics 0.3

Набор проверяет 14 сценариев по шести скиллам: diagnose-metric (3), metrics-memo (2), metrics-system (3: map, experiment, okr), metrics-review (3: каталог, dashboard, vanity), metric-catalog (2), metrics-setup (1). Два промпта на английском проверяют английские триггеры.

В каждом кейсе: grader `tool_used` на вызов скилла (индикатор срабатывания), regex-проверки обязательных слов, один `llm` grader с критериями, для read-only кейсов проверка, что Write и Edit не вызывались.

## Запуск

Из каталога плагина, цель до вариативных флагов:

```
claude plugin eval . --trust-plugin --scaffold --allow-tools Write Edit Bash --model sonnet -j 2 --threshold 0.8 --max-cost-usd 5 --no-publish
```

Подмножество: `--case 'diagnose-*'` или `--tag memo`. Быстрый прогон: `--runs 1 --ablation none`.

## Фикстуры

Кейсы с каталогом содержат `case.yaml` и `scaffold.sh` в папке кейса. Поле `context.scaffold_script` - путь к этому файлу внутри папки кейса, не текст скрипта и не `../`. Скрипт берёт путь к плагину от своего расположения (`$HERE/../../shared/examples`), копирует учебный каталог в `./metrics` рабочей папки и пишет `CLAUDE.md` со ссылкой на него. Абсолютных путей нет. Без `--scaffold` такие кейсы не получат каталог и провалятся.

## Стоимость и шум

По умолчанию 2 запуска на кейс, до 20 ходов. Полный прогон на sonnet занимает порядка нескольких долларов, ограничивайте `--max-cost-usd`.

LLM-graders шумят (судья haiku, ответы агента разные), поэтому порог 0.8, а не 1.0. Одиночный провал разберите по результатам в `evals/results/`, прежде чем править скилл.
