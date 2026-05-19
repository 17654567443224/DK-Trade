from typing import List

import random

from Quant_Engine.template.open_position_template.target import ArrayManager
from Quant_Engine.template.open_position_template.template.customize import Customize


class randomStrategy:
    def __init__(self, position):
        self.position = position
        self.choice = [0, 1]

    def base_random(self):
        return random.randint(0, 1)

    def target_weight_random(self, percent):  # target / rand
        res = self.customize.creat_strategy()
        if not res and res != False:
            if res == 0:
                weights = [percent, 1-percent]
            else:
                weights = [1 - percent, percent]
            return random.choices(self.choice, weights)

    def position_weight_random(self, position_count, percent):
        if len(self.position) < position_count:
            return self.base_random()
        long_porfit = 0
        short_porfit = 0
        for i in self.position[position_count:]:
            ...


    
