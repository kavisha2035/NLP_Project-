pairs=133  gold conflicts=7  align=tfidf  nli=heuristic

| system | P | R | F1 | #pred |
|---|---|---|---|---|
| 1. NLI only (no alignment) | 0.11 | 0.71 | 0.20 | 44 |
| 2. NLI + alignment | 1.00 | 0.71 | 0.83 | 5 |
| 3. STN temporal only | 1.00 | 0.29 | 0.44 | 2 |
| 4. Full: alignment + STN + NLI | 1.00 | 1.00 | 1.00 | 7 |

Event alignment (aligned pairs vs gold same-event pairs): P=1.00 R=1.00 F1=1.00

Full-system errors:
  FP: []
  FN: []