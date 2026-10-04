---
type: regex
target: last_message
pattern: '(?:доли?|доле)\s+успех|success\s*rate'
flags: i
match: contains
weight: 1
---

Названа доля успеха как парная метрика.
