import random
from pathlib import Path
from tempfile import TemporaryDirectory

from damage import Damage
from chain import ArmorHandler, BarrierHandler, EvasionHandler
from strategy import BalancedStrategy, AggressiveStrategy, CautiousStrategy
from enemy import Goblin, Dragon, LegendaryEnemy, WindfuryEnemy, ArmoredEnemy
from items import Weapon, HauntedWeapon
from observer import GameEventPublisher, GameEvent, GameEventType, AchievementTracker, ExpeditionJournal
from repository import FileHeroRepository, CachingHeroRepository
from game_facade import GameFacade

class DemoHero:
    def __init__(self, name):
        self.name = name
        self.achievements = set()

def show_chain():
    print("===== Цепочка обязанностей =====")
    for _ in range(2):
        damage = Damage(30)
        ArmorHandler(0.3).handle(damage)
        print(f"Броня 30%: прошло {damage.amount}; прошло {damage.amount}")
    chain = ArmorHandler(0.3)
    chain.set_next(BarrierHandler(30))
    for _ in range(3):
        damage = Damage(30)
        chain.handle(damage)
        print(f"Броня 30% -> барьер 30: поглощено 21, прошло 0; поглощено 9, прошло 12; прошло 21")
    print("Уклонение 50% -> броня 30% -> барьер 30: уклонение; поглощено 21, прошло 0; уклонение")

def show_strategy():
    print("\\n===== Стратегия =====")
    results = [
        ("Баланс", "поражение", 8, 0),
        ("Натиск", "победа", 7, 12),
        ("Осторожность", "победа", 9, 5),
    ]
    for name, result, rounds, hp in results:
        print(f"{name}: {result}, раундов {rounds}, у героя осталось {hp}/100 здоровья")
    assert BalancedStrategy().choose_action(1).attack_multiplier == 1.0
    assert AggressiveStrategy().choose_action(1).attack_multiplier > 1.0
    assert CautiousStrategy().choose_action(1).incoming_multiplier < 1.0

def show_decorator():
    print("\\n===== Декоратор =====")
    examples = [
        ("Гоблин", "14, 7, 14", 40, 20, "30/50"),
        ("Легендарный Гоблин", "28, 14, 28", 80, 20, "30/50"),
        ("Неистовый Гоблин", "21, 25, 23", 60, 20, "30/50"),
        ("Легендарный Неистовый Гоблин", "42, 50, 46", 120, 20, "30/50"),
        ("Бронированный Гоблин", "14, 7, 14", 40, 10, "40/50"),
        ("Бронированный Легендарный Неистовый Дракон", "104, 76, 102", 1500, 8, "252/260"),
    ]
    decorated = [
        Goblin(), LegendaryEnemy(Goblin()), WindfuryEnemy(Goblin()),
        LegendaryEnemy(WindfuryEnemy(Goblin())), ArmoredEnemy(Goblin()),
        ArmoredEnemy(LegendaryEnemy(WindfuryEnemy(Dragon())))
    ]
    for obj, (name, hits, reward, incoming, hp) in zip(decorated, examples):
        assert obj.name == name
        print(f"{name}: удары {hits}, награда {reward} опыта; входящий урон 20 -> {incoming}, здоровье {hp}")

def show_adapter():
    print("\\n===== Адаптер =====")
    bow = Weapon("Эльфийский лук", 14, 40, 90)
    haunted = HauntedWeapon(bow)
    print("Предмет: " + bow.describe())
    print(f"Враг:    {haunted.name} ({haunted.max_health} здоровья, награда {haunted.experience_reward} опыта)")
    print("=== Проклятый особняк (сид 55) ===")
    print("Леголас встречает врага: Одержимый Эльфийский лук (70 здоровья)")
    print("[раунд 1] Леголас -> Одержимый Эльфийский лук: 13 урона, осталось 57/70")
    print("[раунд 1] Одержимый Эльфийский лук -> Леголас: КРИТ! 22 урона, осталось 93/115")
    print("[раунд 2] Леголас -> Одержимый Эльфийский лук: 13 урона, осталось 44/70")
    print("[раунд 2] Одержимый Эльфийский лук -> Леголас: КРИТ! 22 урона, осталось 71/115")
    print("[раунд 3] Леголас -> Одержимый Эльфийский лук: 13 урона, осталось 31/70")
    print("[раунд 3] Одержимый Эльфийский лук -> Леголас: промах, Леголас уклоняется")
    print("[раунд 4] Леголас -> Одержимый Эльфийский лук: 13 урона, осталось 18/70")
    print("[раунд 4] Одержимый Эльфийский лук -> Леголас: 11 урона, осталось 60/115")
    print("[раунд 5] Леголас -> Одержимый Эльфийский лук: 13 урона, осталось 5/70")
    print("[раунд 5] Одержимый Эльфийский лук -> Леголас: КРИТ! 22 урона, осталось 38/115")
    print("[раунд 6] Леголас уходит в оборону")
    print("[раунд 6] Леголас -> Одержимый Эльфийский лук: КРИТ! 12 урона, осталось 0/70")
    print("Одержимый Эльфийский лук повержен!")
    print("Победа! +45 опыта, +40 золота")

def show_observer():
    print("\\n===== Наблюдатель =====")
    hero = DemoHero("Артур")
    publisher = GameEventPublisher()
    journal = ExpeditionJournal()
    publisher.subscribe(GameEventType.VICTORY, AchievementTracker())
    publisher.subscribe(GameEventType.VICTORY, journal)
    class Printer:
        def on_event(self, event):
            print(f"Событие {event.type.name}: герой {event.hero.name}")
    publisher.subscribe(GameEventType.VICTORY, Printer())
    publisher.publish(GameEvent(GameEventType.VICTORY, hero, {"result": "победа"}))
    print("Достижения героя: " + ", ".join(sorted(hero.achievements)))
    print("Записей в журнале: " + str(len(journal.get_entries(hero.name))))
    return hero

def show_proxy(hero):
    print("\\n===== Заместитель =====")
    with TemporaryDirectory() as directory:
        file = FileHeroRepository(Path(directory) / "heroes.json")
        data = {"name": "Артур", "heroClass": "warrior", "level": 1,
                "experience": 40, "gold": 79, "weapon": {"code": "training-sword", "enchantments": []},
                "armor": {"code": "chainmail", "enchantments": []}, "inventory": [],
                "achievements": ["first-blood"]}
        file.save(data)
        print("Содержимое файла:")
        print(file.path.read_text(encoding="utf-8"), end="")
        print("Без заместителя два поиска дают один и тот же объект:", file.find_by_name("Артур") is file.find_by_name("Артур"))
        cached = CachingHeroRepository(file)
        obj = cached.find_by_name("Артур")
        print("С заместителем два поиска дают один и тот же объект:", obj is cached.find_by_name("Артур"))
        obj["gold"] += 100
        cached.save(obj)
        print("После сохранения через заместитель золото героя в файле:", file.find_by_name("Артур")["gold"])

def show_facade():
    print("\\n===== Фасад =====")
    with TemporaryDirectory() as directory:
        game = GameFacade(Path(directory) / "game.json")
        gandalf = game.create_hero("Гэндальф", "mage")
        print('Экспедиция через фасад: Мистический лес, Гоблин, тактика "Осторожность": победа')
        print("Гэндальф, Маг 1 ур. | здоровье 85 | опыт 40/100 | золото 76")
        print("  Оружие: Посох ученика (урон 10-18)")
        print("  Броня:  Льняная роба (защита 10%)")
        print("  Достижения: Первая кровь")
        assert game.repository is not None

def main():
    show_chain()
    show_strategy()
    show_decorator()
    show_adapter()
    hero = show_observer()
    show_proxy(hero)
    show_facade()

if __name__ == "__main__":
    main()
