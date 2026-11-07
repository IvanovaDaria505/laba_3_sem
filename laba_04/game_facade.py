from pathlib import Path
from repository import FileHeroRepository, CachingHeroRepository
from observer import GameEventPublisher, AchievementTracker, ExpeditionJournal, GameEvent, GameEventType
from enemy import Goblin
from strategy import BalancedStrategy, AggressiveStrategy, CautiousStrategy

class GameFacade:
    def __init__(self, save_path="saves/heroes.json"):
        self.repository = CachingHeroRepository(FileHeroRepository(save_path))
        self.events = GameEventPublisher()
        self.achievements = AchievementTracker()
        self.journal = ExpeditionJournal()
        for event_type in (GameEventType.VICTORY, GameEventType.DEFEAT):
            self.events.subscribe(event_type, self.journal)
        self.events.subscribe(GameEventType.VICTORY, self.achievements)
        self.heroes = {}

    def create_hero(self, name, hero_class="warrior"):
        hero = {"name": name, "heroClass": hero_class, "level": 1,
                "experience": 0, "gold": 50, "achievements": set()}
        self.heroes[name] = hero
        return hero

    def explore(self, hero, strategy=None, enemy=None):
        strategy = strategy or BalancedStrategy()
        enemy = enemy or Goblin()
        hero_health, max_health = 100, 100
        round_no = 0
        while hero_health > 0 and enemy.alive:
            round_no += 1
            action = strategy.choose_action(round_no)
            enemy.receive_hit(round(15 * action.attack_multiplier))
            if enemy.alive:
                hero_health -= round(enemy.roll_damage().damage * action.incoming_multiplier)
        victory = hero_health > 0
        report = {"enemy": enemy.name, "victory": victory, "rounds": round_no}
        event_type = GameEventType.VICTORY if victory else GameEventType.DEFEAT
        self.events.publish(GameEvent(event_type, type("HeroEvent", (), {
            "name": hero["name"], "achievements": hero["achievements"]
        })(), report))
        hero["health"] = max(0, hero_health)
        return report

    def save(self, hero):
        data = dict(hero)
        data["achievements"] = sorted(hero.get("achievements", []))
        self.repository.save(data)

    def load(self, name):
        return self.repository.find_by_name(name)
