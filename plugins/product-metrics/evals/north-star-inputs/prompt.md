---
name: north-star-inputs
tags: [north-star, inputs, no-catalog]
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
---

Our North Star is the weekly count of customers who completed a repair. We are considering two inputs: the same count expressed in thousands, and the share of estimates approved before repair. Build the NSM input tree. We have definitions but no historical data yet.
