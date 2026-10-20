# Experiment results — synthetic print shop

## Context
Simulated visitor-level randomized experiment comparing the existing quote/checkout form (`control`) with a simplified design (`treatment`). Conversion means submitting an order request.

## Checks
- Unique visitor IDs: yes; binary conversion: yes.
- Allocation: control **9,014**, treatment **8,986**.
- Sample-ratio-mismatch diagnostic (50/50 allocation, exact binomial test): **p=0.8405**; inspect instrumentation if unexpectedly small.

## Primary metric
- Control conversion: **7.54%** (680/9,014).
- Treatment conversion: **9.29%** (835/8,986).
- Absolute lift: **+1.748 percentage points**.
- Relative lift: **+23.18%**.
- Two-sided two-proportion z-test: **z=4.224, p=0.000024**.
- 95% Newcombe confidence interval for absolute lift: **[+0.938, +2.561] percentage points**.

## Decision
Observed positive lift with a CI above zero; consider a controlled rollout after checking economics and experiment quality.

## Planning note
Approximate sample size per group for a fresh experiment with baseline 7.54%, MDE=1.0 percentage point, 80% power and alpha=.05: **10,949** (planning illustration only; calculated using observed baseline).

## Caveats
This is synthetic, not a real deployed test. Randomization was simulated at visitor level and we do not have actual revenue, cost, guardrail metrics, repeat exposure or long-term retention. A significant result alone does not establish ROI. Segment analyses should be labeled exploratory and account for multiple comparisons.
