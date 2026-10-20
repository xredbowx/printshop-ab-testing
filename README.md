# PrintWorks — Checkout A/B Test

**Portfolio case study | 100% synthetic data | Fictional packaging/printing company**

## Business question
Does a simplified quote/checkout form increase the proportion of visitors submitting an order request?

## Experiment design
- Unit of randomization/analysis: **unique visitor**; one row per visitor.
- `control`: existing form; `treatment`: simplified form.
- Primary metric: conversion = 1 if an order request was submitted, 0 otherwise. **Not paid-order conversion**.
- Two-sided H0: treatment and control conversion proportions are equal.
- Alpha 0.05; z-test for two proportions; 95% Newcombe CI for risk difference.
- Sample ratio mismatch check versus 50/50 assignment.

## Run
```bash
python -m pip install -r requirements.txt
python scripts/analyze.py
```

## Outputs
- [`outputs/findings.md`](outputs/findings.md) — generated statistical report and decision
- [`outputs/conversion_comparison.png`](outputs/conversion_comparison.png) — conversion comparison
- [`outputs/lift_ci.png`](outputs/lift_ci.png) — difference and confidence interval
- [`outputs/group_summary.csv`](outputs/group_summary.csv) — aggregated metrics

## Interpretation rules
A p-value is not the probability that H0 is true. An insignificant result is not proof of equality. A statistically significant lift need not justify rollout without costs, operational capacity, quality of leads, and guardrails.

## Limitations
All observations and the underlying treatment effect were **simulated** to demonstrate methods, not to represent a real production test. No claims of actual business uplift should be made.

## Interview talking points
Randomization and sample-ratio mismatch, absolute versus relative lift, Type I/II error, power, minimum detectable effect, confidence intervals, post-hoc slices vs preregistered hypotheses, decision quality.
