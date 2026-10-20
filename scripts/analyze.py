from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, binomtest
from statsmodels.stats.proportion import proportions_ztest, confint_proportions_2indep
BASE=Path(__file__).resolve().parents[1]
df=pd.read_csv(BASE/'data/experiment.csv')
assert df.visitor_id.is_unique, 'Duplicate visitor IDs'
assert df.converted.isin([0,1]).all(), 'Invalid conversion indicator'
assert set(df.variant)=={'control','treatment'}
summary=df.groupby('variant').converted.agg(['sum','count','mean'])
n1=int(summary.loc['treatment','count']);n0=int(summary.loc['control','count'])
x1=int(summary.loc['treatment','sum']);x0=int(summary.loc['control','sum'])
p1=x1/n1;p0=x0/n0;diff=p1-p0;rel=diff/p0
z,p=proportions_ztest([x1,x0],[n1,n0],alternative='two-sided')
lo,hi=confint_proportions_2indep(x1,n1,x0,n0,compare='diff',method='newcomb')
srm_p=binomtest(n1,n1+n0,.5).pvalue
# Sample size estimate using conventional approximation for 80% power, two-sided 5% alpha
# Illustrative pre-test sizing for a 1 percentage-point minimum detectable effect
z_alpha=norm.ppf(.975);z_beta=norm.ppf(.8);baseline=p0;mde=.01
n_per_group=(2*(z_alpha+z_beta)**2*baseline*(1-baseline)/mde**2)
summary.rename(columns={'sum':'conversions','count':'visitors','mean':'conversion_rate'}).to_csv(BASE/'outputs/group_summary.csv')
fig,ax=plt.subplots(figsize=(8,5))
labels=['Control','Treatment'];vals=np.array([p0,p1])*100
ax.bar(labels,vals,color=['#64748b','#137C83'],width=.52)
ax.set_ylabel('Conversion rate (%)');ax.set_title('Print shop checkout experiment')
for i,v in enumerate(vals):ax.text(i,v+.08,f'{v:.2f}%',ha='center',fontweight='bold')
ax.set_ylim(0,max(vals)*1.25);fig.tight_layout();fig.savefig(BASE/'outputs/conversion_comparison.png',dpi=175);plt.close(fig)
fig,ax=plt.subplots(figsize=(8,3.5))
ax.errorbar([diff*100],[0],xerr=np.array([[(diff-lo)*100],[(hi-diff)*100]]),fmt='o',capsize=6,color='#137C83')
ax.axvline(0,color='#b91c1c',linestyle='--',label='No effect');ax.set_yticks([]);ax.set_xlabel('Treatment – control (percentage points)')
ax.set_title('Absolute lift with 95% confidence interval');ax.legend();fig.tight_layout();fig.savefig(BASE/'outputs/lift_ci.png',dpi=175);plt.close(fig)
recommendation=('Observed positive lift with a CI above zero; consider a controlled rollout after checking economics and experiment quality.' if lo>0 else 'Evidence is insufficient for positive lift at 5%; do not claim the redesign wins. Consider further testing.')
report=f"""# Experiment results — synthetic print shop

## Context
Simulated visitor-level randomized experiment comparing the existing quote/checkout form (`control`) with a simplified design (`treatment`). Conversion means submitting an order request.

## Checks
- Unique visitor IDs: yes; binary conversion: yes.
- Allocation: control **{n0:,}**, treatment **{n1:,}**.
- Sample-ratio-mismatch diagnostic (50/50 allocation, exact binomial test): **p={srm_p:.4f}**; inspect instrumentation if unexpectedly small.

## Primary metric
- Control conversion: **{p0:.2%}** ({x0:,}/{n0:,}).
- Treatment conversion: **{p1:.2%}** ({x1:,}/{n1:,}).
- Absolute lift: **{diff*100:+.3f} percentage points**.
- Relative lift: **{rel:+.2%}**.
- Two-sided two-proportion z-test: **z={z:.3f}, p={p:.6f}**.
- 95% Newcombe confidence interval for absolute lift: **[{lo*100:+.3f}, {hi*100:+.3f}] percentage points**.

## Decision
{recommendation}

## Planning note
Approximate sample size per group for a fresh experiment with baseline {p0:.2%}, MDE=1.0 percentage point, 80% power and alpha=.05: **{n_per_group:,.0f}** (planning illustration only; calculated using observed baseline).

## Caveats
This is synthetic, not a real deployed test. Randomization was simulated at visitor level and we do not have actual revenue, cost, guardrail metrics, repeat exposure or long-term retention. A significant result alone does not establish ROI. Segment analyses should be labeled exploratory and account for multiple comparisons.
"""
(BASE/'outputs/findings.md').write_text(report,encoding='utf-8');print(report)
