# Q15: AI Tutor Safeguards Optimizer | LearnLoop

LearnLoop gives students aged 10–16 an AI tutor that logs performance and chats. This tool splits a safeguard budget across consent, filters, moderation, privacy and audits.

**Legal / ethics note:** Children’s data needs verifiable parental consent and no profiling; the EU AI Act treats education as high-risk.

Default inputs (illustrative): `[["Parental consent & age check", 300, 20, 1], ["Content safety filters", 250, 25, 1], ["Human moderation", 200, 40, 1], ["Data minimisation", 220, 30, 1], ["Bias & pedagogy audit", 100, 15, 1]]` with budget 100 ₹ lakh

## Engine C - diminishing-returns allocation (Q2, Q7, Q8, Q9, Q12, Q15)
value_i(x) = ceiling_i * (1 - e^(-x/scale_i)) * value_per_unit_i      (concave)
x = 0; repeat 3000 times: add budget/3000 to the option with the largest marginal gain
(respecting max share per option). Optimal for concave curves. Baseline = equal split.
AI Optimizer: scan budget 50%..200%; pick max of value - unit_cost * budget.

Assumptions to replace with real data: normal score distributions (A), exponential amounts and perfect human review (B), saturating curves (C), constant elasticity (D).
