import json
import math


# Loads the data
with open('data\\modules.json') as f:
    data = json.loads(f.read())

hull_ship = data['hull_ship']
hull_carrier = data['hull_carrier']
hull_station = data['hull_station']
modules = data['modules']


# noinspection PyUnboundLocalVariable
def generate_ship(vessel_modules, vessel_tl, vessel_name, vessel_type='ship'):
    vessel = {"type": vessel_type,
              "name": vessel_name,
              "class": "",
              "hs": 0,
              "cost": 0,
              "tl": vessel_tl,
              "turn": 0,
              "modules": vessel_modules,
              "speed": [0, 0]}

    ht_index = {'pre_ind': 0.3, 'ind1': 0.6, 'ind2': 0.9,
                'ht1': 1.1, 'ht2': 1.2, 'ht3': 1.3, 'ht4': 1.4, 'ht5': 1.5,
                'ht6': 1.6, 'ht7': 1.7, 'ht8': 1.8, 'ht9': 1.9, 'ht10': 2.0,
                'ht11': 2.1, 'ht12': 2.2, 'ht13': 2.3, 'ht14': 2.4, 'ht15': 2.5,
                'ht16': 2.6, 'ht17': 2.7, 'ht18': 2.8, 'ht19': 2.9}

    if vessel_type == 'ship':
        hull_sizes = hull_ship
    elif vessel_type == 'carrier':
        hull_sizes = hull_carrier
    elif vessel_type == "station":
        hull_sizes = hull_station

    for module in vessel_modules:
        vessel["cost"] += modules[module]['cost']
        vessel["hs"] += modules[module]['hs']

        if ht_index[modules[module]['tl']] > ht_index[vessel_tl]:
            print('Module ' + module + ' is of a higher tech level than available.')

    for hull_size in hull_sizes:
        if hull_sizes[hull_size]['min'] <= vessel["hs"] <= hull_sizes[hull_size]['max']:
            vessel["cost"] += math.ceil(vessel["hs"]) * hull_sizes[hull_size]['cost']
            vessel["class"] = hull_size
            vessel["turn"] = hull_sizes[hull_size]['turn']

            if ht_index[hull_sizes[hull_size]['tl']] > ht_index[vessel_tl]:
                print('Ship size larger than allowed by tech level.')

    return vessel


class Craft:
    def __init__(self, design, upkeep, hp, modules):
        self.design = design
        self.upkeep = upkeep
        self.hp_max = hp
        self.hp_current = hp
        self.modules = modules
        self.location[0, 0, 0]

    def damage(self, weapon, distance):
        self.hp_current = self.hp_current - 1

    def calculate_upkeep(self):
        self.upkeep = 1

    def

