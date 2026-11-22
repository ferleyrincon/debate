"""Bot for the `conflict` app (stage 2: four one-shot conflict games).

`NUM_ROUNDS = 4`, so `play_round` runs four times per participant. `Introduction`
is shown only in round 1 and `TotalResult` only in the last round; the free chat on
`Decision` is optional and the bot ignores it.
"""

import random

from otree.api import Bot, expect

from . import *


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction
            # Set in `Introduction.before_next_page` from the group fields.
            expect(self.participant.vars['selected_round'] in [1, 2, 3, 4], True)

        yield Decision, dict(cooperate=random.choice([True, False]))

        # `set_payoffs` runs in `ResultsWaitPage.after_all_players_arrive`.
        expect(self.player.payoff is not None, True)

        if self.round_number == C.NUM_ROUNDS:
            yield TotalResult, dict(
                descrip_cooperate='Elegi pensando en lo que haria la otra persona.'
            )
