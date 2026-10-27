# Cross-Document Narrative Timeline Synthesis and Conflict Detection (Neuro-Symbolic NLP)

Topic: Gulf of Tonkin incident, Aug 1964, as told by three sources (US government, North Vietnam, a retrospective analysis).

## Setup and run
```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python main.py     # timeline + conflicts + out/graph.html
python eval.py     # P/R/F1 table -> out/results.md
```
First run downloads `all-MiniLM-L6-v2` and `cross-encoder/nli-deberta-v3-small` (needs internet).
If a download fails the code falls back to TF-IDF (alignment) and a number/negation heuristic (NLI);
the header of every output prints `align=` and `nli=` so you can see which mode ran.

## Pipeline
| Step | File | Type | What it does |
|---|---|---|---|
| 1 Ingest | data/docs.json | - | sources with `src`, `pub` date, `sents` |
| 2 Extract + normalize time | ext.py | neural (spaCy) | one event per sentence, DATE entities -> day intervals via dateparser; "two days later" -> offset to previous event |
| 3 Align events | align.py | neural | sentence embeddings + same-date bonus, greedy cross-source merge, one sentence per source per cluster |
| 4 Temporal reasoning | stn.py | symbolic | Simple Temporal Network. Floyd-Warshall gives each source's implied interval per event; Bellman-Ford finds negative cycles = minimal explanation |
| 5 Claim conflicts | nli.py | neural | DeBERTa NLI on aligned cross-source pairs (both directions) |
| 6 Synthesis | main.py | - | consensus interval = intersection of sources; empty = conflict; timeline.md, conflicts.json, graph.html |
| 7 Evaluation | eval.py, data/gold.json | - | 4 systems vs hand labels |

Key point: the "two days later" sentence has no date of its own, so NLI cannot see the conflict. The STN derives its
date from the relative offset and exposes it. NLI catches the claim conflicts ("no second attack"), the STN cannot.
That complementarity is the neuro-symbolic result.

## Data note (important)
`docs.json` holds condensed paraphrases written for this project, not verbatim articles. C3 ("Two days later") is a
planted discrepancy and not a historical claim. For the report, replace or extend the sentences with real excerpts
(Wikipedia, the 2005 NSA historical study, Hanoi's statements), keep the sentence ids in `gold.json` in sync, and
add more gold pairs.

## Known limitations
- Sentence = event (no sub-sentence events); only day-granularity dates; "before/after" clauses not parsed.
- Offsets are relative to the previous sentence only.
- Gold set is small (7 conflicts out of 133 cross-source pairs), so F1 is coarse. Add pairs before quoting numbers.
