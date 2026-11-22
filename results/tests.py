"""Bot for the `results` app (IRI questionnaire, background survey, payment page).

`Survey` has the 28 items of Davis's Interpersonal Reactivity Index on a 1-5 scale;
`Survey_2` has the 14 background questions; `Final` shows the computed payment and
the link to the payment form.
"""

import random

from otree.api import Bot, Submission, expect

from . import *


IRI_FIELDS = ['p_selection_{}'.format(i) for i in range(1, 29)]


class PlayerBot(Bot):
    def play_round(self):
        yield Survey, {f: random.choice([1, 2, 3, 4, 5]) for f in IRI_FIELDS}

        yield Survey_2, dict(
            age=random.randint(17, 30),
            gender_sex=random.choice([0, 1, 2]),
            major=random.randint(1, 63),
            semester=random.randint(0, 13),
            stratum=random.randint(0, 6),
            experiments=random.choice([0, 1]),
            income=random.randrange(50000, 500000, 10000),
            mother_educ=random.choice([0, 1, 2, 3, 4, 5]),
            father_educ=random.choice([0, 1, 2, 3, 4, 5]),
            income_stair=random.randint(1, 10),
            risk_measure=random.randint(0, 10),
            G_trust=random.randint(0, 10),
            patience=random.randint(1, 5),
            punish_justice=random.randint(1, 4),
        )

        # Total payment is computed in `Survey_2.before_next_page`.
        expect(self.player.payoff_complete >= C.SHOWFEE, True)

        # `Final` is the last page and has no next button: participants read their
        # payment there and left through the external payment form.
        yield Submission(Final, check_html=False)
