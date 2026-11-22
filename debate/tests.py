"""Bot for the `debate` app.

It reproduces the path a participant who consents actually walked in the field:
welcome -> consent -> instructions -> dilemma + initial position -> write the
argument for the side drawn for them -> read the partner's argument -> write the
reply (own side or the opposite side, depending on the arm) -> read the partner's
reply -> social-appropriateness question -> rate four arguments -> stage-1 result.

The bot only yields pages whose `is_displayed()` is true for this player, so the
conditions below must stay in sync with `__init__.py`.
"""

import random

from otree.api import Bot, Submission, expect

from . import *


# Long enough to satisfy the "at least 5 words" instruction shown to participants
# (the instruction is a label, not a server-side validation).
TEXTO_FAVOR = (
    'Los estudiantes deberian seguir denunciando porque la contaminacion del agua '
    'afecta la salud de toda la comunidad y callar solo protege a quienes se '
    'benefician de las actividades ilegales.'
)
TEXTO_CONTRA = (
    'Los estudiantes no deberian seguir denunciando porque las amenazas armadas '
    'ponen en riesgo sus vidas y existen otras formas mas seguras de proteger la '
    'cienaga sin exponerse.'
)
TEXTO_REPLICA_FAVOR = (
    'Mantengo que hay que denunciar: el riesgo existe, pero la comunidad ya se '
    'esta sumando y abandonar la denuncia deja el problema intacto para todos.'
)
TEXTO_REPLICA_CONTRA = (
    'Insisto en no denunciar: la vida de los estudiantes vale mas que una denuncia '
    'y hay rutas institucionales que no los exponen a los grupos armados.'
)

# The four amounts the participant had to distribute among the four arguments.
ASIGNACIONES = [0, 2000, 4000, 6000]


class PlayerBot(Bot):
    def play_round(self):
        yield Bienvenida

        # Everyone in the bot run consents; participants who did not consent were
        # sent straight to `Agradecimiento` and produced no further data.
        yield Consentimiento, dict(consentimiento=True)

        yield Inst_iniciales

        yield Lectura_Dilema, dict(
            posicion_afin=random.choice([True, False]),
            exp_emp=random.choice([1, 2, 3, 4]),
        )

        yield Inicio_debate

        # `agree` is the side drawn for this player in `creating_session`:
        # True = A FAVOR DE DENUNCIAR, False = EN CONTRA DE DENUNCIAR.
        agree = self.player.agree
        expect(agree in (True, False), True)

        # The four writing pages have no next button in the template: they rely on
        # `timeout_seconds` to advance, so the HTML check has to be disabled.
        if agree == 1:
            yield Submission(
                Afavor, dict(arg_a_favor=TEXTO_FAVOR), check_html=False
            )
        else:
            yield Submission(
                Encontra, dict(arg_en_contra=TEXTO_CONTRA), check_html=False
            )

        yield Leer_argumento

        # Round 2. Arm 1 (two perspectives): the player argues the *other* side.
        # Arm 0 (one perspective): the player replies keeping their own side.
        treatment = self.player.group.treatment
        if (treatment == 1 and agree == 0) or (treatment == 0 and agree == 1):
            yield Submission(
                Replica_afavor,
                dict(rep_a_favor=TEXTO_REPLICA_FAVOR),
                check_html=False,
            )
        elif (treatment == 1 and agree == 1) or (treatment == 0 and agree == 0):
            yield Submission(
                Replica_encontra,
                dict(rep_en_contra=TEXTO_REPLICA_CONTRA),
                check_html=False,
            )

        yield Leer_argumento_replica

        yield Posicion_final, dict(posicion_final=random.choice([1, 2, 3, 4]))

        yield Instr_calificacion

        # The real page is a drag-and-drop ranking that writes the four amounts into
        # hidden inputs; the bot submits a random permutation of the same amounts.
        montos = random.sample(ASIGNACIONES, 4)
        yield Calificacion, dict(
            calificacion_usted=montos[0],
            calificacion_pareja=montos[1],
            calificacion_jugador_afavor=montos[2],
            calificacion_jugador_encontra=montos[3],
        )

        yield Siguiente_etapa, dict(
            descrip_calificacion='Valore primero la claridad y luego los datos concretos.'
        )

        # Stage-1 payments must be filled in by now (`set_pagocalificacion` runs in
        # `Siguiente_etapa.vars_for_template`).
        expect(self.player.pago_cal_usted is not None, True)
        expect(self.player.pago_aprobacion_social in (0, 4000), True)
