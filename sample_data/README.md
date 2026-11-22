# Synthetic sample data

These files were produced by the oTree bots (`debate/tests.py`, `conflict/tests.py`,
`results/tests.py`) with `python sample_data/generate_sample_data.py` (4 bot
participants = 2 pairs). Every value is a random bot answer: **no participant data**.
Use them to see the structure of the exports.

| File | Rows | Content |
|---|---|---|
| `all_apps_wide.csv` | 1 per participant | oTree wide export (all apps, all rounds) |
| `debate.csv` | 1 per participant | stage 1: assigned side, consent, initial and final position, the four ratings and the stage-1 payments; group columns hold the four texts |
| `conflict.csv` | 1 per participant and round (4 rounds) | stage 2: `player.cooperate` (A = True), `player.payoff`, `group.levels`, `group.selected_round` |
| `results.csv` | 1 per participant | the 28 IRI items, the 14 background questions and `payoff_complete` |

The argument texts are the two fixed sentences written in the bots, not real
arguments. Ratings, positions, cooperation choices and survey answers are random, so
these files cannot be used to reproduce any result in the paper.

The chat messages of the `conflict` app are not here: the bots do not use the chat.
In a real session they are downloaded separately from the admin ("Chat messages").

Regenerate with:

```bash
python sample_data/generate_sample_data.py
```

It runs the bots against a temporary SQLite database, so `db.sqlite3` is untouched.
