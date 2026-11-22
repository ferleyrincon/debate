"""
Generate the SYNTHETIC sample data in this folder by running the oTree bots.

Run from the repository root (same environment as `otree test`):

    python sample_data/generate_sample_data.py

It uses a throw-away SQLite database in a temporary folder (it never touches
db.sqlite3), plays one 'debate_conflict' session with N bot participants
(debate/tests.py, conflict/tests.py and results/tests.py) and copies the exports
into this folder:

    sample_data/all_apps_wide.csv   one row per participant (oTree wide export)
    sample_data/debate.csv          one row per participant (stage 1)
    sample_data/conflict.csv        one row per participant and round (4 rounds)
    sample_data/results.csv         one row per participant (questionnaires)

All values are random bot answers. No participant data are produced or included.

The chat messages of the `conflict` app are not exported here: the bots do not use
the chat, and in the admin they are downloaded separately ("Chat messages").
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

N_PARTICIPANTS = 4          # must be a multiple of 4 (see AGENTS.md)
SESSION_CONFIG = 'debate_conflict'
FILES = ['all_apps_wide.csv', 'debate.csv', 'conflict.csv', 'results.csv']

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent

tmp_dir = Path(tempfile.mkdtemp())
tmp_db = tmp_dir / 'synthetic.sqlite3'
export_dir = tmp_dir / 'export'

env = dict(os.environ)
env['DATABASE_URL'] = 'sqlite:///' + tmp_db.as_posix()
env.setdefault('OTREE_ADMIN_PASSWORD', 'dev')
env['PYTHONIOENCODING'] = 'utf-8'

# `python -m otree` is not supported in oTree 5, so call the `otree` console script
# that sits next to the interpreter running this file.
otree_exe = shutil.which('otree') or str(
    Path(sys.executable).parent / ('otree.exe' if os.name == 'nt' else 'otree')
)
cmd = [
    otree_exe, 'test',
    SESSION_CONFIG, str(N_PARTICIPANTS),
    '--export', str(export_dir),
]
print('running:', ' '.join(cmd))
subprocess.run(cmd, cwd=str(ROOT), env=env, check=True)

for name in FILES:
    src = export_dir / name
    if not src.exists():
        raise SystemExit('missing export: {}'.format(src))
    shutil.copyfile(src, OUT / name)
    print('wrote', OUT / name)

shutil.rmtree(tmp_dir, ignore_errors=True)
