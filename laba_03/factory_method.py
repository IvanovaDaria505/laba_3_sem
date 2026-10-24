from abc import ABC, abstractmethod

from singleton import Dice
from prototype import ItemCatalog, SHARP, FIERY
from hero import Hero
from enemies import Enemy


class Location(ABC):
    name = "Неизвестная локация"

    @abstractmethod
    def create_enemy(self) -> Enemy:
        """Фабричный метод создания противника."""
        pass

    def explore(
        self,
        hero: Hero,
        catalog: ItemCatalog
    ):
        dice = Dice.get_instance()
        hero.restore()
        enemy = self.create_enemy()

        print(f"\n=== {self.name} ===")
        print(
            f"{hero.name} встречает противника: "
            f"{enemy.name} ({enemy.health} HP)"
        )

        round_number = 1

        while hero.alive() and enemy.health > 0:
            damage = hero.attack()
            dealt = enemy.receive_hit(damage)

            print(
                f"[Раунд {round_number}] "
                f"{hero.name} наносит {dealt} урона. "
                f"У врага осталось {enemy.health} HP."
            )

            if enemy.health <= 0:
                break

            damage = enemy.attack()
            dealt = hero.receive_hit(damage)

            print(
                f"[Раунд {round_number}] "
                f"{enemy.name} наносит {dealt} урона. "
                f"У героя осталось "
                f"{hero.health}/{hero.max_health} HP."
            )

            round_number += 1

        if hero.alive():
            hero.experience += enemy.experience

            reward = dice.roll(
                enemy.gold // 2,
                enemy.gold
            )

            hero.gold += reward

            print(
                f"Победа! +{enemy.experience} опыта, "
                f"+{reward} золота."
            )

            if hero.experience >= hero.level * 100:
                hero.experience -= hero.level * 100
                hero.level += 1
                hero.max_health += 15
                hero.restore()

                print(f"Новый уровень: {hero.level}!")

            if dice.chance(0.60):
                loot = catalog.create(
                    dice.pick([
                        "iron_sword",
                        "dragon_blade",
                        "bow",
                        "staff"
                    ])
                )

                if dice.chance(0.30):
                    loot.enchant(
                        dice.pick([SHARP, FIERY])
                    )

                print("Найдена добыча:", loot.describe())

            else:
                print("Добычи в этот раз нет.")

        else:
            lost = hero.gold // 2
            hero.gold -= lost

            print(
                f"Поражение. Потеряно {lost} золота."
            )

        hero.show()


class Forest(Location):
    name = "Мистический лес"

    def create_enemy(self) -> Enemy:
        return Enemy(
            "Гоблин",
            50,
            6,
            14,
            40,
            30
        )


class Crypt(Location):
    name = "Заброшенный склеп"

    def create_enemy(self) -> Enemy:
        return Enemy(
            "Скелет",
            110,
            10,
            24,
            90,
            70,
            resistance=0.30
        )


class DragonLair(Location):
    name = "Логово дракона"

    def create_enemy(self) -> Enemy:
        return Enemy(
            "Древний дракон",
            260,
            16,
            22,
            500,
            400,
            resistance=0.25,
            fire_chance=0.25
        )