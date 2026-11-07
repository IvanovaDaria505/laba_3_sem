from dataclasses import dataclass
from enemy import Hit

@dataclass
class Weapon:
    name: str
    damage: int
    crit_chance: int = 0
    price: int = 90

    def roll_damage(self):
        return Hit(self.damage)

    def describe(self):
        return f"{self.name} (урон {self.damage}, шанс крита {self.crit_chance}%)"

class HauntedWeapon:
    HEALTH_PER_DAMAGE = 5

    def __init__(self, weapon: Weapon):
        self.weapon = weapon
        self.name = "Одержимый " + weapon.name
        self.max_health = weapon.damage * self.HEALTH_PER_DAMAGE
        self.health = self.max_health
        self.experience_reward = weapon.price // 2

    def roll_damage(self):
        return self.weapon.roll_damage()

    def receive_hit(self, amount):
        self.health = max(0, self.health - amount)
        return amount

    @property
    def alive(self):
        return self.health > 0
