# Hawks and doves exchanging ideas: oTree code for an argument exchange, a paid rating of arguments and four conflict games

Replication code for the lab experiment analyzed in the working paper:

> Rincón, F., et al. (2026). *Arguing both sides changes cooperation by less than the effect of communication itself: a preregistered null result, with exploratory bounds on peer rewards.* Working paper, version 1.1 (draft, not publicly circulated). Preregistration: AsPredicted #201318 (26 November 2024).
>
> `TODO (Ferley):` final author list and CRediT roles (authorship is still open; candidates in the paper's contribution note are Carrillo, Villarreal, Bermúdez, Rincón and Cortés). The oTree code in this repository was written by José David García P. (commits `5880513` and `dc00292`).

This repository contains only the code that participants used. **It does not contain participant data**, and real data must never be added to it. `sample_data/` holds synthetic output produced by the bots. The pilot CSV files that used to be in this repository were removed in November 2026; they belong to the paper's private data folder.

## 1. The experiment

- **Population:** 148 university students in 74 fixed pairs (73 women, 75 men; mean age 21.4; sex recorded in two categories, gender identity not measured).
- **Place:** REBEL, the experimental economics laboratory of Universidad del Rosario, Bogotá, Colombia.
- **Field dates:** 4 sessions on 26 and 29 November and 2 December 2024. The code deployed in the field is the content of commit `dc00292` ("Final Version", 7 January 2025), which after the November 2026 history purge is commit `5015de8`. The commit is dated **after** the sessions, so it is the final version uploaded afterwards, not a snapshot taken on the day. See section «Is this the field version?» below.
- **What participants did in oTree:** 21 pages in three apps, all in Spanish (see [`docs/`](docs/)):
  1. `debate` — welcome, informed consent, general instructions, the Ciénaga Grande de Santa Marta dilemma plus their own initial position, the argument for the side drawn for them (5-minute cap), reading the partner's argument, the round-2 reply, reading the partner's reply, the social-appropriateness question, and a paid ranking in which they distributed 6000 / 4000 / 2000 / 0 pesos among four arguments (their own, their partner's and two from another pair).
  2. `conflict` — four one-shot 2×2 conflict games with the same partner, with a free chat on each decision page.
  3. `results` — the 28 items of Davis's Interpersonal Reactivity Index, 14 background questions, and the final page with the computed payment and the link to the payment form.

**Why `PD_Chat` appears in the URLs.** The session config is called `debate_conflict`, but the `conflict` app sets `NAME_IN_URL = 'PD_Chat'` (`conflict/__init__.py`). So participant URLs read `/p/<code>/PD_Chat/Decision/30`, the page order in the oTree monitor shows `PD_Chat/...`, and the chat channel ids use `PD_Chat`. The data exports, by contrast, use the app name: `conflict.csv` and `conflict.1.player.cooperate`.

## 2. Design

| Arm in the working paper | What happened in round 2 of stage 1 | Session config | How the arm is recorded |
|---|---|---|---|
| **Two perspectives** (treatment) | Each participant wrote a second argument defending **the other** side | `debate_conflict` | `debate.Group.treatment = True` → page `Replica_afavor` for the player whose drawn side was *en contra*, `Replica_encontra` for the player whose drawn side was *a favor* |
| **One perspective** (control) | Each participant replied **keeping** the side drawn for them | `debate_conflict` | `debate.Group.treatment = False` → page `Replica_afavor` for the player whose drawn side was *a favor*, `Replica_encontra` for the other |

`TODO (Ferley):` the number of pairs per arm in the final sample (the paper reports 148 participants in 74 pairs but not the split by arm in this file).

**Random assignment happens inside oTree**, in `creating_session` of [`debate/__init__.py`](debate/__init__.py):

- **Arm, by pair.** `treatments = [1]*(n_groups // 2) + [0]*(n_groups // 2)`, then `random.shuffle(treatments)` and one value per group. The split is exactly half and half, so the number of pairs in a session must be even (participants a multiple of 4). With an odd number of pairs, `zip` leaves the last group with `treatment = None` and neither reply page is shown.
- **Side, by participant within the pair.** Player 1 gets `agree = random.choice([True, False])` (`True` = *A FAVOR DE DENUNCIAR*, `False` = *EN CONTRA DE DENUNCIAR*) and player 2 gets the opposite, so every pair always has one participant per side.
- **Which four arguments each participant rates.** `set_argumento` pairs groups two by two (`groups[i]`, `groups[i+1]`) and swaps their round-1 arguments, so each participant rates their own argument, their partner's, and the argument of a same-side stranger plus that of an opposite-side stranger from the neighbouring pair.
- **Order of the four conflict games and the paid game.** `creating_session` of [`conflict/__init__.py`](conflict/__init__.py) draws `group.selected_round = random.randint(1, 4)` and a shuffled `group.levels` of `[0, 1, 2, 3]`. Both are stored in `participant.vars` on the `Introduction` page of round 1, so the round-1 draw is the one that governs the whole stage.

### The four conflict games

`conflict/__init__.py` fixes mutual A at 16000 and mutual B at 4000, and varies the mixed outcomes:

| Level index | X | Y |
|---|---|---|
| 0 | 8000 | 8000 |
| 1 | 8000 | 0 |
| 2 | 24000 | 8000 |
| 3 | 24000 | 0 |

In `Decision.html` the participant who chooses A while the partner chooses B receives `y_value` and the one who chooses B receives `x_value`, which is what `get_payoff_for_round` does (A = cooperate → `Y_VALUES`, B = defect → `X_VALUES`).

### Known issues in the field code (not fixed here)

These are reproduced as deployed, because the repository's job is to replicate the field version. They matter for anyone analysing the data.

1. **The order shown and the order paid can differ.** `Decision.vars_for_template` picks the level with the shuffled order (`levels[round_number - 1]`), but `get_payoff_for_round` indexes `X_VALUES`/`Y_VALUES` with `round_number - 1` directly. Whenever the round-1 `levels` draw is not `0,1,2,3`, the X and Y shown on screen are not the ones used to pay the mixed outcomes. Mutual A (16000) and mutual B (4000) are unaffected. This is visible in `sample_data/conflict.csv`.
2. **`levels` and `selected_round` are redrawn every round.** `creating_session` runs once per round, so `conflict.2/3/4.group.levels` and `...selected_round` hold draws that were never used. Only the round-1 values were stored in `participant.vars` and used. Use the round-1 columns.
3. **The generic instructions page swaps X and Y.** `conflict/instructions.html` puts X in the cell of the participant who chooses A, while `Decision.html` and the payoff code put Y there.
4. **The writing pages announce four minutes but allow five.** `Inicio_debate.html` says «cuatro minutos»; `timeout_seconds = 5*60` on `Afavor`, `Encontra`, `Replica_afavor` and `Replica_encontra`.
5. **`REAL_WORLD_CURRENCY_CODE = 'USD'`** in `settings.py`, while every amount shown to participants is written as Colombian pesos in the templates. `USE_POINTS = False`, so oTree formats `payoff` with a dollar sign in the admin; the numbers are pesos.
6. **Two declarations are never used:** `Group.has_arrived` (`debate/__init__.py`, declared with `initial=False` and never written, so it is always `False` in the data) and `C.ENDOWMENT = cu(10000)` (declared and never read; the 10000-peso show-up fee that is actually paid is `results.C.SHOWFEE`).

`TODO (Ferley):` item 1 is the open point listed in the paper's contribution note as «matriz de pago del juego sorteado en oTree». Decide whether the analysis of the mixed-outcome payoffs uses the matrix shown or the matrix paid, and state it in the paper.

## 3. Requirements and installation

- Python **3.9** (tested with 3.9.25). The field server pinned `python-3.9.16` in `runtime.txt`, which was removed from this package.
- **oTree 5.10.4** (the version used in the field) and the exact versions in [`requirements.txt`](requirements.txt).

```bash
python3.9 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

`requests` is in `requirements.txt` because the oTree 5 bot runner needs it.

For a server deployment set `OTREE_PRODUCTION=1`, `OTREE_SECRET_KEY`, `OTREE_ADMIN_PASSWORD` and a `DATABASE_URL`, run `otree resetdb` once and then `otree prodserver`. PostgreSQL also needs `pip install psycopg2-binary`; the field repository pinned `psycopg2>=2.8.4`, which is not needed to replicate locally with SQLite.

## 4. Running the experiment and the bots

```bash
otree devserver                   # then open http://localhost:8000 and start a demo of "debate_conflict"
otree test debate_conflict 4      # bots: 4 participants (2 pairs) through all 21 pages
```

`otree test` must finish with `Bots completed session` and no traceback. The number of participants must be a multiple of 4 (see section 2: the arm split needs an even number of pairs, and the argument swap needs pairs of pairs).

The bots are in `debate/tests.py`, `conflict/tests.py` and `results/tests.py`. Four pages are submitted with `check_html=False` because their templates have no next button: the three writing pages rely on `timeout_seconds`, and `results/Final` is the last page.

`python sample_data/generate_sample_data.py` reruns the bots against a temporary database and rewrites the synthetic CSV files in `sample_data/`.

## 5. Data produced

| Table | Rows | Main variables |
|---|---|---|
| `debate` (oTree app export) | 1 per participant | `player.agree` (side drawn: True = *a favor*), `player.consentimiento`, `player.posicion_afin` (own initial position), `player.exp_emp` (how they chose it), `player.posicion_final` (social appropriateness, 1–4), the four ratings `player.calificacion_usted` / `_pareja` / `_jugador_afavor` / `_jugador_encontra`, `player.calificacion_otros`, `player.pago_cal_usted`, `player.pago_aprobacion_social` (4000 or 0), `player.descrip_calificacion`; group columns `group.treatment` (arm), `group.arg_a_favor`, `group.arg_en_contra`, `group.rep_a_favor`, `group.rep_en_contra` (the four texts), `group.arg_cal_afavor`, `group.arg_cal_contra` (the two texts received from the neighbouring pair), `group.has_arrived` (unused) |
| `conflict` (oTree app export, named `PD_Chat` in the URLs) | 1 per participant and round, 4 rounds | `player.cooperate` (True = option A), `player.payoff`, `player.descrip_cooperate` (round 4 only), `group.levels`, `group.selected_round` (use the round-1 values, see «Known issues») |
| `results` (oTree app export) | 1 per participant | the 28 IRI items `player.p_selection_1`–`_28` (1–5), `player.age`, `player.gender_sex`, `player.major`, `player.semester`, `player.stratum`, `player.experiments`, `player.income`, `player.mother_educ`, `player.father_educ`, `player.income_stair`, `player.risk_measure`, `player.G_trust`, `player.patience`, `player.punish_justice`, `player.payoff_complete` (10000 show-up fee + the paid conflict game + the stage-1 rating payment + the social-approval payment) |
| Chat messages | 1 per message | nickname, channel and text of the free chat on the `conflict` decision pages. `TODO (Ferley):` the paper states the free chat was not analyzed |

That is 21 fields in `debate`, 4 in `conflict` and 43 in `results`. The full list with the labels participants saw is in [`docs/diccionario_variables.md`](docs/diccionario_variables.md).

**Exporting the data**

- Standard tables: oTree admin → *Data* (all apps wide, per app, page times).
- Chat messages: oTree admin → *Data* → *Chat messages*.
- From the bots: `otree test debate_conflict 4 --export <folder>`.

Exported files (`*.csv`, `*.xlsx`, `*.json`, `*.gz`) are ignored by git, except the synthetic files in `sample_data/`.

## 6. Based on

The code is original to this project; it is not a fork of a published oTree repository. Two parts follow standard oTree material:

- The `conflict` app has the shape of oTree's textbook prisoner's-dilemma example (a single `cooperate` BooleanField rendered as two buttons, `other_player`/`set_payoff` helpers, a `ResultsWaitPage` with `after_all_players_arrive`) plus oTree's built-in `{{ chat }}` component and four payoff levels of our own. `TODO (Ferley):` confirm whether it started from oTree's sample game or from another repository, so the credit can be exact.
- `_static/persist-raw.js` is oTree's documented snippet for keeping form inputs across page reloads.
- The 28 items of the Interpersonal Reactivity Index are Davis's instrument in its Spanish wording (see section 7); the scale is not ours.

A later, extended version of this experiment (session configs `debate_conflict` and `debate_conflict_donantes`, apps `eet1`/`eet2`) exists outside this repository under `JoseDGarciaP/ExperimentoOtreeDanielVillar`. That repository is not part of this replication package.

## 7. How to cite

If you use this code, please cite it (see [`CITATION.cff`](CITATION.cff)) together with:

- This repository: Rincón, F., et al. (2026). *Code for: Arguing both sides changes cooperation by less than the effect of communication itself* (version 1.0.0) [Computer software]. https://github.com/ferleyrincon/debate
- oTree: Chen, D. L., Schonger, M., & Wickens, C. (2016). oTree—An open-source platform for laboratory, online, and field experiments. *Journal of Behavioral and Experimental Finance, 9*, 88–97. https://doi.org/10.1016/j.jbef.2015.12.001
- The questionnaire: Davis, M. H. (1983). Measuring individual differences in empathy: Evidence for a multidimensional approach. *Journal of Personality and Social Psychology, 44*(1), 113–126. https://doi.org/10.1037/0022-3514.44.1.113

`TODO (Ferley):` the Spanish IRI wording used in `results/__init__.py` comes from a published Spanish adaptation; add that reference.

## 8. License

MIT (see [`LICENSE`](LICENSE)). Participant data are not part of this repository and are not covered by this license. `TODO (Ferley):` the copyright line reads «2024 ferleyrincon»; the oTree code was written by José David García P., so confirm the holder with him.

## Is this the field version?

**Very probably yes, but the raw field export is missing to confirm it.** What can be checked today:

- The pilot export of 8 November 2024 matches this code field by field: 21 fields in `debate`, 4 in `conflict`, 43 in `results`.
- The processed field dataset contains 62 of the 68 fields of this repository. The six missing ones (`descrip_cooperate`, `exp_emp`, `has_arrived`, `levels`, `posicion_final`, `selected_round`) look renamed or dropped during cleaning, not absent from the instrument.
- The "Final Version" commit is from 7 January 2025, after the four sessions.
- There is no commit between 17 October 2024 and 7 January 2025, so it cannot be proven that nothing changed between sessions.

Confirming it would need the raw oTree export of the four field sessions.
