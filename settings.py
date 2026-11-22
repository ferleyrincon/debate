# oTree settings for the Hawks-and-doves lab study (REBEL, Universidad del Rosario,
# Bogota, 26 and 29 November and 2 December 2024).
#
# One session config, the one used in the field:
#   debate_conflict = debate (argument exchange and paid rating of four arguments)
#                     -> conflict (four one-shot conflict games with the same partner)
#                     -> results (IRI questionnaire, background survey, payment page).
# It runs with 4 participants per session in the demo (the field sessions were larger);
# the number of participants must be a multiple of 4, see AGENTS.md.
#
# Note: the `conflict` app sets NAME_IN_URL = 'PD_Chat', so participant URLs and the
# per-app export of that app are named `PD_Chat`, not `conflict`.
#
# Removed in 2026 for the replication package: the empty ROOMS list and the Heroku
# deployment files (Procfile, runtime.txt).

from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)

SESSION_CONFIGS = [
    dict(
        name='debate_conflict',
        num_demo_participants=4,
        app_sequence=['debate', 'conflict', 'results'],
    )
]

LANGUAGE_CODE = 'es'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

ADMIN_USERNAME = 'admin'
# for security, set the admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'dev-only-change-in-production')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
