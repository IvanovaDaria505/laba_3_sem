from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class Action:
    name: str
    attack_multiplier: float
    incoming_multiplier: float

class CombatStrategy(ABC):
    name = "Тактика"

    @abstractmethod
    def choose_action(self, round_number: int) -> Action:
        raise NotImplementedError

class BalancedStrategy(CombatStrategy):
    name = "Баланс"
    def choose_action(self, round_number):
        return Action("обычная атака", 1.0, 1.0)

class AggressiveStrategy(CombatStrategy):
    name = "Натиск"
    def choose_action(self, round_number):
        return Action("мощная атака", 1.5, 1.5)

class CautiousStrategy(CombatStrategy):
    name = "Осторожность"
    def choose_action(self, round_number):
        return Action("защита", 0.8, 0.65)
