from dataclasses import dataclass
from enum import Enum, auto

class GameEventType(Enum):
    VICTORY = auto()
    DEFEAT = auto()
    LEVEL_UP = auto()

@dataclass
class GameEvent:
    type: GameEventType
    hero: object
    report: object = None

class GameEventPublisher:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, observer):
        self._subscribers.setdefault(event_type, []).append(observer)

    def publish(self, event):
        for observer in tuple(self._subscribers.get(event.type, [])):
            observer.on_event(event)

class AchievementTracker:
    def on_event(self, event):
        if event.type == GameEventType.VICTORY:
            event.hero.achievements.add("Первая кровь")

class ExpeditionJournal:
    def __init__(self):
        self.entries = {}

    def on_event(self, event):
        self.entries.setdefault(event.hero.name, []).append(event.report)

    def get_entries(self, name):
        return list(self.entries.get(name, []))
