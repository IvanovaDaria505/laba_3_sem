import random

class Dice:

    _instance = None #сначала экземпляр не создан

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._random = random.Random()
        return cls._instance

    @classmethod
    def get_instance(cls) -> "Dice":
        return cls()

    def reseed(self, seed: int) -> None:
        self._random.seed(seed)

    def roll(self, minimum: int, maximum: int) -> int:
        return self._random.randint(minimum, maximum)

    def chance(self, probability: float) -> bool:
        return self._random.random() < probability

    def pick(self, options):
        if not options:
            raise ValueError(
                "Нельзя выбрать элемент из пустого списка"
            )
        return self._random.choice(options)