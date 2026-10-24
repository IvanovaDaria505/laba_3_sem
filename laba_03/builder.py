from hero import Hero
from abstract_factory import StarterKitFactory


class HeroBuilder:

    def __init__(self):
        self.name = None
        self.hero_class = None
        self.kit = None
        self.level = 1
        self.gold = 50

    def set_name(self, name: str) -> "HeroBuilder":
        self.name = name.strip()
        return self

    def set_class(self, hero_class: str) -> "HeroBuilder":
        self.hero_class = hero_class
        return self

    def set_starter_kit(
        self, kit: StarterKitFactory
    ) -> "HeroBuilder":
        self.kit = kit
        return self

    def set_level(self, level: int) -> "HeroBuilder":
        self.level = level
        return self

    def set_gold(self, gold: int) -> "HeroBuilder":
        self.gold = gold
        return self

    def build(self) -> Hero:
        if not self.name:
            raise ValueError("У героя должно быть имя")

        if len(self.name) > 20:
            raise ValueError(
                "Имя не может быть длиннее 20 символов"
            )

        if self.hero_class not in (
            "Воин", "Следопыт", "Маг"
        ):
            raise ValueError(
                "Не выбран класс героя"
            )

        if self.kit is None:
            raise ValueError(
                "Не задан стартовый набор"
            )

        if self.level < 1 or self.gold < 0:
            raise ValueError(
                "Уровень должен быть положительным, "
                "золото — неотрицательным"
            )

        health = {
            "Воин": 120,
            "Следопыт": 100,
            "Маг": 85
        }[self.hero_class]

        return Hero(
            self.name,
            self.hero_class,
            health,
            self.kit.create_weapon(),
            self.kit.create_armor(),
            self.level,
            self.gold
        )