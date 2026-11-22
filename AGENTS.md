# AGENTS.md

Instructions for AI agents (and humans) working on this repository. Every statement below can be checked against the files named.

## 1. Purpose

- This repository is the oTree code of one lab experiment: an argument exchange on a moral dilemma, a paid ranking of four arguments and four one-shot conflict games with the same partner, run with 148 university students in 74 pairs at REBEL (Universidad del Rosario, Bogotá) on 26 and 29 November and 2 December 2024 (see `README.md`).
- Its job is to let others **replicate the field version exactly** or **adapt it** to a new study.
- It contains no participant data. Do not add real data, exports, databases or credentials; `sample_data/` holds synthetic bot output only. The pilot CSV files that used to live in the root were removed in November 2026.
- One session config exists: `debate_conflict` (`app_sequence = ['debate', 'conflict', 'results']`), 4 demo participants. The arm is assigned by oTree, per pair, in `creating_session` of `debate/__init__.py` (`Group.treatment`). The side each participant defends is assigned there too (`Player.agree`).
- **The number of participants must be a multiple of 4.** The arm split is exactly half the pairs, and the argument swap works on consecutive pairs of pairs.

## 2. File map

| File | Controls |
|---|---|
| `settings.py` | `SESSION_CONFIGS` (only `debate_conflict`), `LANGUAGE_CODE = 'es'`, `REAL_WORLD_CURRENCY_CODE = 'USD'` (amounts shown are pesos), `USE_POINTS = False`, secret key and admin password from `OTREE_SECRET_KEY` / `OTREE_ADMIN_PASSWORD` |
| `debate/__init__.py` | `C.ENDOWMENT`, `C.FAVOR` / `C.CONTRA` (the two side labels), `Group.treatment`, the four argument fields and the two received texts, `Player.agree` (side drawn), `consentimiento`, `posicion_afin`, `exp_emp`, `posicion_final`, the four `calificacion_*` fields and the two payments; the functions `creating_session` (arm and side draw), `set_argumento` (swap of arguments between neighbouring pairs), `set_pagocalificacion` (rating payment) and `set_calcular_moda_global` (modal answer for the social-approval payment); `page_sequence` of 20 page classes |
| `debate/*.html` | All stage-1 texts in Spanish, including the dilemma (`Lectura_Dilema.html`) and the drag-and-drop rating page (`Calificacion.html`, which writes the four amounts into hidden inputs and hides oTree's next button) |
| `conflict/__init__.py` | `C.NAME_IN_URL = 'PD_Chat'`, `C.NUM_ROUNDS = 4`, `MUTUAL_COOPERATE`/`MUTUAL_DEFECT`, `X_VALUES`/`Y_VALUES`/`ORDER`, `Group.levels` and `Group.selected_round`, `Player.cooperate` and `descrip_cooperate`, `get_payoff_for_round`, `set_payoffs`; `page_sequence = [Introduction, Decision, ResultsWaitPage, TotalResult]` |
| `conflict/*.html` | Stage-2 texts; `Decision.html` holds the payoff table, the two submit buttons for A/B and oTree's `{{ chat }}`; `instructions.html` is included by `Introduction.html` |
| `results/__init__.py` | `C.SHOWFEE = 10000`, the 28 IRI items with their Spanish wording, the 14 background fields, `payoff_complete`; `page_sequence = [Survey, Survey_2, Final]` |
| `results/*.html` | Questionnaire layout and the final payment page (which prints `participant.code` and links to the external payment form) |
| `debate/tests.py`, `conflict/tests.py`, `results/tests.py` | Bots, one per app |
| `_templates/global/Page.html`, `_static/global/results.css`, `_static/persist-raw.js` | oTree base template with a larger body font; CSS of the final page; oTree's snippet to keep inputs across reloads |
| `docs/` | Page-by-page description of what participants saw and the variable dictionary |
| `sample_data/` | Synthetic CSVs and `generate_sample_data.py` |
| `requirements.txt` | Exact versions (oTree 5.10.4, Python 3.9) |

## 3. What to adapt

The code is original to this project, so there is no upstream repository to diff against. What an adapter has to touch:

| File | What it fixes in this study | What an adapter must change |
|---|---|---|
| `debate/Lectura_Dilema.html` | The Ciénaga Grande de Santa Marta dilemma and the initial-position question | The dilemma text; the two sides in `C.FAVOR` / `C.CONTRA` must match it |
| `debate/__init__.py`, `creating_session` | Half the pairs to each arm, one participant per side | Keep an even number of pairs, or rewrite the `zip` so no group is left with `treatment = None` |
| `debate/__init__.py`, `set_argumento` | Which stranger arguments each participant rates | Rewrite if you want more than one stranger pair, or a different matching |
| `debate/Instr_calificacion.html`, `debate/Calificacion.html` | The four amounts (6000 / 4000 / 2000 / 0) and the drag-and-drop ranking | The amounts in the template **and** in the bot; the page has no server-side check that the four values are different |
| `debate/__init__.py`, `set_calcular_moda_global` | 4000 pesos if the answer matches the modal answer of the whole session | The amount and the question (`posicion_final`) |
| `conflict/__init__.py` | Four payoff levels and the paid game drawn at random | `X_VALUES`, `Y_VALUES`, `NUM_ROUNDS` and the amounts written as text in `Decision.html` and `instructions.html` |
| `results/__init__.py` | IRI (28 items) and the background questions | The whole questionnaire; `major` is a 63-option list specific to Colombian universities |
| `results/Final.html` | Shows the payment and links to a Google Form | **Replace the form link.** The form collected names, ID numbers and bank accounts |
| `settings.py` | One session config, Spanish, no rooms | Session name, `app_sequence`, language, currency |
| `requirements.txt` | oTree 5.10.4 on Python 3.9 | Keep the pins unless you re-test everything |

**Warnings:**

- `conflict` pays with `X_VALUES`/`Y_VALUES` indexed by `round_number - 1`, while `Decision.html` shows the level given by the shuffled `group.levels`. They disagree whenever the round-1 draw is not `0,1,2,3`. Do not "fix" this in the replication branch; it is what the participants faced. See `README.md`, «Known issues in the field code».
- `creating_session` of `conflict` redraws `levels` and `selected_round` in every round, but only the round-1 values are used (they are copied to `participant.vars` on `Introduction`).
- `Consentimiento.error_message` blocks the participant who answers «No acepto»; `Agradecimiento` is the only page shown to them. Every other page in `debate` is guarded by `is_displayed: return player.consentimiento`, so a bot must consent.
- `debate/Afavor.html`, `Encontra.html`, `Replica_afavor.html` and `Replica_encontra.html` have **no next button** (they rely on `timeout_seconds = 5*60`), and `results/Final.html` is the last page with no button either. Bots must submit these five pages with `Submission(..., check_html=False)`.
- `Calificacion.html` hides oTree's next button with CSS and uses its own `<button type="submit">`; the four values travel in hidden inputs filled by JavaScript.

After any change: update the bots in `*/tests.py` and run `otree test debate_conflict 4`.

## 4. Do not change if you want to replicate the field version

- The dilemma text and the two side labels (`debate/Lectura_Dilema.html`, `C.FAVOR` / `C.CONTRA`).
- The page order in the three `page_sequence` lists and the `is_displayed` conditions of `Replica_afavor` / `Replica_encontra`, which are what defines the two arms.
- The draw in `creating_session` of `debate/__init__.py`: half the pairs per arm, one participant per side.
- `X_VALUES = [8000, 8000, 24000, 24000]`, `Y_VALUES = [8000, 0, 8000, 0]`, `MUTUAL_COOPERATE = 16000`, `MUTUAL_DEFECT = 4000`, `NUM_ROUNDS = 4` and the indexing bug described above.
- The four rating amounts (6000 / 4000 / 2000 / 0), the 4000-peso social-approval payment and `C.SHOWFEE = 10000`.
- The 28 IRI items and their 1–5 scale, and the 14 background questions.
- `timeout_seconds = 5*60` on the four writing pages.
- The versions in `requirements.txt` (oTree 5.10.4 on Python 3.9).

## 5. Mandatory check before any commit

```bash
pip install -r requirements.txt     # Python 3.9
otree test debate_conflict 4
```

The run must end with `Bots completed session` and no traceback. Also confirm that `git status` shows no `db.sqlite3`, `*.csv` outside `sample_data/`, `*.xlsx`, `*.gz`, `*.json` or `.env` files.
