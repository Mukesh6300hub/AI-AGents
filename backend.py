"""Backend - Q15: AI Tutor Safeguards Optimizer | LearnLoop
Run: pip install fastapi uvicorn && uvicorn backend:app --reload   (docs at /docs)
GET /preset -> default inputs   GET /optimize/default -> run on defaults   GET /ai-optimizer -> best setting   POST /optimize -> run on your inputs
"""
import math
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Q15 AI Tutor Safeguards Optimizer - LearnLoop")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
Phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

class Opt(BaseModel):
    name: str; ceil: float; scale: float; value: float


class C(BaseModel):  # diminishing-returns allocation
    budget: float; options: List[Opt]


def engine_c(q: C):
    x = [0.0] * len(q.options); step = q.budget / 4000
    f = lambda o, v: o.ceil * (1 - math.exp(-v / o.scale)) * o.value
    for _ in range(4000):
        gains = [f(o, x[i] + step) - f(o, x[i]) for i, o in enumerate(q.options)]
        x[gains.index(max(gains))] += step
    eq = sum(f(o, q.budget / len(x)) for o in q.options)
    tot = sum(f(o, v) for o, v in zip(q.options, x))
    return {"allocation": {o.name: round(v, 2) for o, v in zip(q.options, x)},
            "total_value": tot, "equal_split_value": eq, "uplift_pct": (tot / eq - 1) * 100}


PRESET = {
  "n": 15,
  "name": "AI Tutor Safeguards Optimizer",
  "company": "LearnLoop",
  "desc": "LearnLoop gives students aged 10–16 an AI tutor that logs performance and chats. This tool splits a safeguard budget across consent, filters, moderation, privacy and audits.",
  "eng": "C",
  "bud": 100,
  "unit": "₹ lakh",
  "uc": 1,
  "opts": [
    [
      "Parental consent & age check",
      300,
      20,
      1
    ],
    [
      "Content safety filters",
      250,
      25,
      1
    ],
    [
      "Human moderation",
      200,
      40,
      1
    ],
    [
      "Data minimisation",
      220,
      30,
      1
    ],
    [
      "Bias & pedagogy audit",
      100,
      15,
      1
    ]
  ],
  "tip": "Children’s data needs verifiable parental consent and no profiling; the EU AI Act treats education as high-risk."
}


@app.get("/preset")
def preset():
    return PRESET


@app.post("/optimize")
def optimize(q: C):
    return engine_c(q)


@app.get("/optimize/default")
def optimize_default():
    v = PRESET.get("v")
    a = C(budget=PRESET["bud"], options=[Opt(name=o[0], ceil=o[1], scale=o[2], value=o[3]) for o in PRESET["opts"]])
    return engine_c(a)


@app.get("/ai-optimizer")
def ai_optimizer():
    from optimizer import best_settings  # imported lazily to avoid a circular import
    return best_settings()
