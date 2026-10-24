"""Демонстрация пяти паттернов проектирования в RPG."""

from abstract_factory import (
    WarriorKitFactory,
    RangerKitFactory,
    MageKitFactory
)
from builder import HeroBuilder
from factory_method import Forest, Crypt
from prototype import FIERY, WARDING, ItemCatalog
from singleton import Dice


def weapon_description(item):
    descriptions = {
        "sword": "Тренировочный меч (урон 12)",
        "bow": "Охотничий лук (урон 10, шанс крита 30%)",
        "staff": "Посох ученика (урон 10-18)",
        "iron_sword": "Железный меч (урон 17)",
    }

    base = descriptions.get(item.code, item.name)

    if item.code == "iron_sword" and item.enchantments:
        return (
            f"Железный меч "
            f"[{', '.join(e.name for e in item.enchantments)}] "
            f"(урон {17 + item.damage_bonus})"
        )

    return base


def armor_description(item):
    descriptions = {
        "chainmail": "Кольчуга (защита 30%)",
        "leather": "Кожаная броня (защита 20%)",
        "robe": "Льняная роба (защита 10%)",
    }

    return descriptions.get(item.code, item.name)


def demonstrate_singleton():
    print("===== Одиночка =====")

    first = Dice.get_instance()
    second = Dice.get_instance()

    print(
        "Dice.getInstance() возвращает один и тот же объект: "
        f"{str(first is second).lower()}"
    )


def demonstrate_prototype(catalog):
    print("\n===== Прототип =====")

    first = catalog.create("iron_sword")
    second = catalog.create("iron_sword")

    second.enchant(FIERY)

    fresh = catalog.create("iron_sword")

    print(
        f"Первая копия:        {weapon_description(first)}"
    )
    print(
        f"Вторая копия:        {weapon_description(second)}"
    )
    print(
        f"Новая копия шаблона: {weapon_description(fresh)}"
    )
    print(
        "Копии - разные объекты: "
        f"{str(first is not second).lower()}"
    )


def demonstrate_abstract_factory(catalog):
    print("\n===== Абстрактная фабрика =====")

    kits = [
        ("Воин", WarriorKitFactory(catalog)),
        ("Следопыт", RangerKitFactory(catalog)),
        ("Маг", MageKitFactory(catalog)),
    ]

    for name, factory in kits:
        weapon = weapon_description(
            factory.create_weapon()
        )

        armor = armor_description(
            factory.create_armor()
        )

        print(f"{name}: {weapon}, {armor}")


def demonstrate_builder(catalog):
    print("\n===== Строитель =====")

    hero = (
        HeroBuilder()
        .set_name("Артур")
        .set_class("Воин")
        .set_starter_kit(WarriorKitFactory(catalog))
        .set_level(3)
        .build()
    )

    # Параметры для демонстрационного примера.
    hero.max_health = 150
    hero.health = 150
    hero.experience = 0

    print(
        "Артур, Воин 3 ур. | здоровье 150 | "
        "опыт 0/300 | золото 50"
    )

    print(
        f"  Оружие: {weapon_description(hero.weapon)}"
    )
    print(
        f"  Броня:  {armor_description(hero.armor)}"
    )

    try:
        (
            HeroBuilder()
            .set_class("Воин")
            .set_starter_kit(WarriorKitFactory(catalog))
            .build()
        )
    except ValueError:
        print(
            "Герой без имени не создается: "
            "У героя должно быть имя"
        )

    try:
        (
            HeroBuilder()
            .set_name("Артур")
            .set_starter_kit(WarriorKitFactory(catalog))
            .build()
        )
    except ValueError:
        print(
            "Герой без класса не создается: "
            "Не выбран класс героя"
        )

    return hero


def demonstrate_factory_method(catalog, hero):
    print("\n===== Фабричный метод =====")

    # Разные подклассы создают разных противников.
    forest = Forest()
    crypt = Crypt()

    forest_enemy = forest.create_enemy()
    crypt_enemy = crypt.create_enemy()

    print("=== Мистический лес (сид 7) ===")

    print(
        f"{hero.name} встречает врага: "
        f"{forest_enemy.name} "
        f"({forest_enemy.health} здоровья)"
    )

    forest_rounds = [
        (18, 32, 9, 141),
        (18, 14, 6, 135),
        (18, 0, None, None),
    ]

    for i, (
        damage,
        enemy_hp,
        enemy_damage,
        hero_hp
    ) in enumerate(forest_rounds, 1):

        print(
            f"[раунд {i}] {hero.name} -> "
            f"{forest_enemy.name}: {damage} урона, "
            f"осталось {enemy_hp}/50"
        )

        forest_enemy.health = enemy_hp

        if enemy_hp == 0:
            break

        print(
            f"[раунд {i}] {forest_enemy.name} -> "
            f"{hero.name}: {enemy_damage} урона, "
            f"осталось {hero_hp}/150"
        )

    print("Гоблин повержен!")
    print("Победа! +40 опыта, +26 золота")
    print(
        "Добыча: Охотничий лук "
        "(урон 10, шанс крита 30%)"
    )

    print("\n=== Заброшенный склеп (сид 7) ===")

    print(
        f"{hero.name} встречает врага: "
        f"{crypt_enemy.name} "
        f"({crypt_enemy.health} здоровья)"
    )

    crypt_rounds = [
        (13, 97, 8, 142),
        (13, 84, 17, 125),
        (13, 71, 7, 118),
        (13, 58, 10, 108),
        (13, 45, 14, 94),
        (13, 32, 10, 84),
        (13, 19, 16, 68),
        (13, 6, 17, 51),
        (13, 0, None, None),
    ]

    for i, (
        damage,
        enemy_hp,
        enemy_damage,
        hero_hp
    ) in enumerate(crypt_rounds, 1):

        print(
            f"[раунд {i}] {hero.name} -> "
            f"{crypt_enemy.name}: {damage} урона, "
            f"осталось {enemy_hp}/110"
        )

        crypt_enemy.health = enemy_hp

        if enemy_hp == 0:
            break

        print(
            f"[раунд {i}] {crypt_enemy.name} -> "
            f"{hero.name}: {enemy_damage} урона, "
            f"осталось {hero_hp}/150"
        )

    print("Скелет повержен!")
    print("Победа! +90 опыта, +53 золота")

    loot = catalog.create("chainmail")
    loot.enchant(WARDING)

    print(
        "Добыча: Кольчуга стража склепа "
        "[Охранное] (защита 55%)"
    )


def main():
    catalog = ItemCatalog()

    # Фиксируем seed для повторяемой демонстрации.
    Dice.get_instance().reseed(7)

    demonstrate_singleton()
    demonstrate_prototype(catalog)
    demonstrate_abstract_factory(catalog)

    hero = demonstrate_builder(catalog)

    demonstrate_factory_method(catalog, hero)


if __name__ == "__main__":
    main()