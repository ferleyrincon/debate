from otree.api import *
import random

c = cu

doc = 'Etapa inicial donde toma lugar un debate entre dos participantes'

class C(BaseConstants):
    NAME_IN_URL = 'debate'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10000)
    FAVOR = 'A favor de que denuncie'
    CONTRA = 'En contra de que denuncie'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    treatment = models.BooleanField()
    arg_a_favor = models.LongStringField(label='Escriba su argumento:')
    arg_en_contra = models.LongStringField(label='Escriba su argumento')
    rep_a_favor = models.LongStringField(label='Escriba su réplica:')
    rep_en_contra = models.LongStringField(label='Escriba su réplica')


class Player(BasePlayer):
    agree = models.BooleanField()
    consentimiento = models.BooleanField(
        choices=[[True, 'Sí'], [False, 'No']],
        label='¿Aceptar términos?', widget=widgets.RadioSelect)
    posicion_afin = models.BooleanField(
        choices=[[True, 'A favor de que denuncie'], [False, 'En contra de que denuncie']],
        label='Escoja la posición con la que se siente identificado', widget=widgets.RadioSelect)
    exp_emp = models.BooleanField(
        choices=[[True, 'A favor de que denuncie'], [False, 'En contra de que denuncie']],
        label='¿Cuál cree que es la posición de la mayoría de los participantes?', widget=widgets.RadioSelect)
    posicion_final = models.BooleanField(
        choices=[[True, 'A favor de que denuncie'], [False, 'En contra de que denuncie']],
        label='Escoja la posición con la que se siente identificado después del debate que tuvo', widget=widgets.RadioSelect)
    exp_empfinal = models.BooleanField(
        choices=[[True, 'A favor de que denuncie'], [False, 'En contra de que denuncie']],
        label='¿Cuál cree que es la posición de la mayoría de los participantes después de haber tenido el debate?', widget=widgets.RadioSelect)


def creating_session(self):
    for group in self.get_groups():
        group.treatment = random.choice([True, False])
        for player in group.get_players():
            if (player.id_in_group == 1):
                player.agree = random.choice([True, False])
            else:
                player.agree = not player.get_others_in_group()[0].agree


class Intro(Page):
    pass


class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['consentimiento']


class Inst_iniciales(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Lectura_Dilema(Page):
    form_model = 'player'
    form_fields = ['posicion_afin', 'exp_emp']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Inicio_debate_favor(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1


class Afavor(Page):
    form_model = 'group'
    form_fields = ['arg_a_favor']
    timeout_seconds = 5*60

    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_a_favor'] = player.group.arg_a_favor


class Inicio_debate_contra(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 2


class Encontra(Page):
    form_model = 'group'
    form_fields = ['arg_en_contra']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 2
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['argumento_en_contra'] = player.group.arg_en_contra


class WaitForPosturaFavor(WaitPage):
    body_text = "En esta actividad, eres quien debate {}. Has sido asignado aleatoriamente con una persona que debate {}.\
                        Por favor, espera a que la persona termine de escribir su argumento".format(C.CONTRA, C.FAVOR)
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 2


class WaitForPosturaContra(WaitPage):
    body_text = "En esta actividad, eres quien debate {}. Has sido asignado aleatoriamente con una persona que debate {}.\
                        Por favor, espera a que la persona termine de escribir su argumento".format(C.FAVOR, C.CONTRA)
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1


class WaitForLecturaContra(WaitPage):
    body_text = "En esta actividad, eres quien debate {}. Has sido asignado aleatoriamente con una persona que debate {}.\
                        Por favor, espera a que la persona termine de escribir su argumento".format(C.FAVOR, C.CONTRA)
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1


class Leer_arg_encontra(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1


class Leer_arg_afavor(Page):
    form_model = 'player'
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 2


class Replica_afavor(Page):
    form_model = 'group'
    form_fields = ['rep_a_favor']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 1


class Replica_encontra(Page):
    form_model = 'group'
    form_fields = ['rep_en_contra']
    timeout_seconds = 5*60
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento and player.id_in_group == 2


class Posicion_final(Page):
    form_model = 'player'
    form_fields = ['posicion_final', 'exp_empfinal']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.consentimiento


class Agradecimiento(Page):
    
    @staticmethod
    def is_displayed(player: Player):
        return not player.consentimiento
    
    @staticmethod
    def vars_for_template(player: Player):
        return { 
            'mensaje_agradecimiento': 'Gracias por tu tiempo. Lamentamos que no puedas continuar con el experimento.'
        }


page_sequence = [
    Intro, 
    Consentimiento, 
    Inst_iniciales, 
    Lectura_Dilema, 
    Inicio_debate_favor, 
    Afavor, 
    WaitForPosturaContra, 
    Inicio_debate_contra, 
    Encontra, 
    WaitForPosturaFavor, 
    WaitForLecturaContra, 
    Leer_arg_encontra, 
    Leer_arg_afavor, 
    Replica_afavor, 
    Replica_encontra, 
    Posicion_final, 
    Agradecimiento
]
