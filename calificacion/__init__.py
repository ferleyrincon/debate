from otree.api import *
import json

doc = """
Your app description
"""

class C(BaseConstants):
    NAME_IN_URL = 'calificacion'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    value_1_1 = models.FloatField(label='')
    value_1_2 = models.FloatField(label='')
    value_2_1 = models.FloatField(label='') 
    value_2_2 = models.FloatField(label='') 
    value_3_1 = models.FloatField(label='')
    value_3_2 = models.FloatField(label='')
    value_4_1 = models.FloatField(label='')
    value_4_2 = models.FloatField(label='')

# PAGES
class Instructions(Page):
    pass

class Lectura_argumentos(Page):
    form_model = 'player'
    form_fields = [
        'value_1_1', 'value_1_2',
        'value_2_1', 'value_2_2',
        'value_3_1', 'value_3_2',
        'value_4_1', 'value_4_2'
    ]



class Results(Page):
    pass


page_sequence = [
    Instructions, 
    Lectura_argumentos, 
    Results
]
