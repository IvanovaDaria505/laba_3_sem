from dataclasses import dataclass

@dataclass
class Damage:
    amount: int
    evaded: bool = False
    absorbed: int = 0

    def absorb(self, value: int):
        actual = min(self.amount, value)
        self.amount -= actual
        self.absorbed += actual

    def evade(self):
        self.amount = 0
        self.evaded = True
