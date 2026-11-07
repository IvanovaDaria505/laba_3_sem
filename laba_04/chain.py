import random
from damage import Damage

class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def pass_next(self, damage):
        if self.next_handler:
            self.next_handler.handle(damage)
        return damage

class ArmorHandler(Handler):
    def __init__(self, defense: float):
        super().__init__()
        self.defense = defense

    def handle(self, damage: Damage):
        damage.absorb(round(damage.amount * self.defense))
        return self.pass_next(damage)

class BarrierHandler(Handler):
    def __init__(self, points: int):
        super().__init__()
        self.points = points

    def handle(self, damage: Damage):
        absorbed = min(self.points, damage.amount)
        self.points -= absorbed
        damage.absorb(absorbed)
        return self.pass_next(damage)

class EvasionHandler(Handler):
    def __init__(self, chance: float, rng=None):
        super().__init__()
        self.chance = chance
        self.rng = rng or random.Random()

    def handle(self, damage: Damage):
        if self.rng.random() < self.chance:
            damage.evade()
            return damage
        return self.pass_next(damage)
