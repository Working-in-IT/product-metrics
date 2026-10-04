---
type: regex
target: last_message
pattern: 'hypothes|гипотез|insufficient|not enough|can.t (?:produce|explain|say)'
flags: i
match: contains
weight: 1
---

Hypothesis wording, or an explicit data-insufficient stop (also valid per the skill).
