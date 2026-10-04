#!/usr/bin/env bash
# Фикстура для eval: копирует учебный каталог плагина в рабочую папку кейса.
# Путь к плагину берётся от расположения этого скрипта, абсолютных путей нет.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cp -R "$HERE/../../shared/examples" ./metrics
printf '%s\n' 'Каталог метрик: metrics/CATALOG.md' > CLAUDE.md
