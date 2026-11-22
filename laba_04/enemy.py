from dataclasses import dataclass


@dataclass
class Hit:
    damage: int


class Enemy:
    def __init__(self, name, health, damage, experience_reward):
        self.name = name
        self.health = health
        self.max_health = health
        self.damage = damage
        self.experience_reward = experience_reward

    def roll_damage(self):
        return Hit(self.damage)

    def receive_hit(self, amount):
        self.health = max(0, self.health - amount)
        return amount

    @property
    def alive(self):
        return self.health > 0


class Goblin(Enemy):
    def __init__(self):
        super().__init__(
            name="Гоблин",
            health=50,
            damage=7,
            experience_reward=40
        )


class Dragon(Enemy):
    def __init__(self):
        super().__init__(
            name="Дракон",
            health=260,
            damage=26,
            experience_reward=500
        )


class EnemyDecorator:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


class LegendaryEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Легендарный " + self.wrapped.name

    def roll_damage(self):
        return Hit(self.wrapped.roll_damage().damage * 2)

    @property
    def experience_reward(self):
        return self.wrapped.experience_reward * 2


class ArmoredEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Бронированный " + self.wrapped.name

    def receive_hit(self, amount):
        return self.wrapped.receive_hit(max(1, amount // 2))


class WindfuryEnemy(EnemyDecorator):
    @property
    def name(self):
        return "Неистовый " + self.wrapped.name

    def roll_damage(self):
        return Hit(self.wrapped.roll_damage().damage * 2)

    @property
    def experience_reward(self):
        return (
            self.wrapped.experience_reward
            + self.wrapped.experience_reward // 2
        )
