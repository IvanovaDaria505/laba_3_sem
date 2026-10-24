from dataclasses import dataclass
from singleton import Dice


@dataclass
class Enemy:
    name: str
    health: int
    min_damage: int
    max_damage: int
    experience: int
    gold: int
    resistance: float = 0.0
    fire_chance: float = 0.0

    def attack(self) -> int:
        damage = Dice.get_instance().roll(
            self.min_damage,
            self.max_damage
        )

        if (
            self.fire_chance
            and Dice.get_instance().chance(
                self.fire_chance
            )
        ):
            print(
                f"{self.name} использует огненное дыхание!"
            )
            damage *= 2

        return damage

    def receive_hit(self, damage: int) -> int:
        actual = max(
            1,
            round(damage * (1 - self.resistance))
        )

        self.health = max(
            0,
            self.health - actual
        )

        return actual