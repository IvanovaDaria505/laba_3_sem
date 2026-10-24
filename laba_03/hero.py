"""Герой игры."""

from dataclasses import dataclass
from singleton import Dice
from prototype import Item


@dataclass
class Hero:
    name: str
    hero_class: str
    max_health: int
    weapon: Item
    armor: Item
    level: int = 1
    gold: int = 50
    experience: int = 0
    health: int = 0

    def __post_init__(self):
        if self.health == 0:
            self.health = self.max_health

    def alive(self) -> bool:
        return self.health > 0

    def attack(self) -> int:
        base = {
            "меч": 12,
            "лук": 10,
            "посох": 14
        }.get(
            {
                "Воин": "меч",
                "Следопыт": "лук",
                "Маг": "посох"
            }.get(self.hero_class, "меч"),
            12
        )

        damage = (
            base
            + self.weapon.damage_bonus
            + (self.level - 1) * 3
        )

        if (
            self.weapon.code == "bow"
            and Dice.get_instance().chance(0.30)
        ):
            print("Критический выстрел!")
            damage *= 2

        elif self.weapon.code == "staff":
            damage = Dice.get_instance().roll(
                max(1, damage - 4),
                damage + 4
            )

        return damage

    def receive_hit(self, damage: int) -> int:
        armor_bonus = {
            "chainmail": 0.30,
            "leather": 0.20,
            "robe": 0.10
        }.get(self.armor.code, 0.0)

        defense = min(
            0.75,
            armor_bonus + self.armor.defense
        )

        actual = max(
            1,
            round(damage * (1 - defense))
        )

        self.health = max(
            0,
            self.health - actual
        )

        return actual

    def restore(self):
        self.health = self.max_health

    def show(self):
        print(
            f"{self.name} — {self.hero_class}, "
            f"уровень {self.level}"
        )

        print(
            f"Здоровье: {self.health}/{self.max_health} | "
            f"Опыт: {self.experience} | Золото: {self.gold}"
        )

        print(
            f"Оружие: {self.weapon.name}; "
            f"броня: {self.armor.name}"
        )