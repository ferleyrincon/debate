
from otree.api import *
import random
c = cu

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 6
    DECISIONES = ['A','B','C','D','E']
    MONTO = 20000
    PAGO_COMP = 7500
    PAGO_COO = 10000
    PAGOS_H = [13000,14000,16000,18000,20000]
    # PAGOS_P = [cu(8000),cu(6000),cu(4000),cu(2000),cu(0)]
    INSTRUCTIONS_TEMPLATE = 'conflict/instructions.html'

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    order_pagos_H = models.StringField()  # Para almacenar la lista aleatorizada como cadena
    order_pagos_P = models.StringField()
    pass

class Player(BasePlayer):
    competir = models.BooleanField(choices=[[True, 'H (Competitiva)'], [False, ' P (Cooperativa)']], doc='Decision del participante', widget=widgets.RadioSelect)
    
# FUNCTIONS
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)

def other_player(player: Player):
    group = player.group
    return player.get_others_in_group()[0]

def set_payoff(player: Player):
    ronda = player.round_number
    pago_H_A = player.session.vars['pagos_h_list'][ronda - 2]
    pago_P_A = player.session.vars['pagos_p_list'][ronda - 2]
    payoff_matrix = {
        (False, True): pago_H_A,
        (True, True): C.PAGO_COMP,
        (False, False): C.PAGO_COO,
        (True, False): pago_P_A,
    }
    other = other_player(player)
    player.payoff = payoff_matrix[(player.competir, other.competir)]

def creating_session(self: Subsession):
    # Aleatorizar la lista
    if self.round_number == 1:
        for g in self.get_groups():
            randomized_list = random.sample(C.PAGOS_H, len(C.PAGOS_H))
        # Crear una nueva constante con la resta de 20000 menos cada elemento en la lista aleatorizada
            self.session.vars['pagos_h_list'] = randomized_list
            self.session.vars['pagos_p_list'] = [20000 - x for x in randomized_list]
            g.order_pagos_H = ",".join(map(str, self.session.vars['pagos_h_list']))
            g.order_pagos_P = ",".join(map(str, self.session.vars['pagos_p_list']))

class Introduction(Page):
    def is_displayed(self):
        # Mostrar solo en la primera ronda
        return self.round_number == 1

class Decision(Page):
    timeout_seconds = 30
    form_model = 'player'
    form_fields = ['competir']
    timer_text = '''Recuerde, si su tiempo se agota, se asumirá que elige la estrategia H (Competitiva). 
    El tiempo restante para terminar la ronda es:'''

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # you may want to fill a default value for any form fields,
            # because otherwise they may be left null.
            player.competir = True
    def vars_for_template(self):
        return dict(
            pago_H_A = self.session.vars['pagos_h_list'][self.round_number - 2],
            pago_P_A = self.session.vars['pagos_p_list'][self.round_number - 2]
        )
    def is_displayed(self):
        # Mostrar solo en la primera ronda
        return self.round_number > 1

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
    def is_displayed(self):
        # Mostrar solo en la primera ronda
        return self.round_number > 1

class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            ronda = player.round_number,
            opponent=opponent,
            same_choice=player.competir == opponent.competir,
            mi_decision=player.field_display('competir'),
            opponent_decision=opponent.field_display('competir'),
        )
    def is_displayed(self):
        # Mostrar solo en la primera ronda
        return self.round_number > 1
    
page_sequence = [
    Introduction, 
    Decision, 
    ResultsWaitPage, 
    Results
]