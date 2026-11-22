import unittest
from unittest.mock import Mock

from enemy import (
    Goblin,
    LegendaryEnemy,
    ArmoredEnemy,
    WindfuryEnemy
)


class TestEnemyDecorator(unittest.TestCase):
    """Структурный паттерн: Декоратор."""

    def test_legendary_enemy_doubles_damage(self):
        enemy = Goblin()
        enemy.roll_damage = Mock(return_value=10)

        decorated = LegendaryEnemy(enemy)

        self.assertEqual(
            decorated.roll_damage(),
            20
        )

        enemy.roll_damage.assert_called_once()

    def test_legendary_enemy_doubles_reward(self):
        enemy = Goblin()
        enemy.reward = Mock(return_value=50)

        decorated = LegendaryEnemy(enemy)

        self.assertEqual(
            decorated.reward(),
            100
        )

        enemy.reward.assert_called_once()

    def test_windfury_enemy_doubles_damage(self):
        enemy = Goblin()
        enemy.roll_damage = Mock(return_value=10)

        decorated = WindfuryEnemy(enemy)

        self.assertEqual(
            decorated.roll_damage(),
            20
        )

    def test_windfury_enemy_increases_reward(self):
        enemy = Goblin()
        enemy.reward = Mock(return_value=100)

        decorated = WindfuryEnemy(enemy)

        self.assertEqual(
            decorated.reward(),
            150
        )

    def test_armored_enemy_reduces_damage(self):
        enemy = Goblin()
        enemy.receive_hit = Mock(return_value=10)

        decorated = ArmoredEnemy(enemy)

        decorated.receive_hit(20)

        enemy.receive_hit.assert_called_once_with(10)

    def test_decorator_preserves_enemy_properties(self):
        enemy = Goblin()
        decorated = LegendaryEnemy(enemy)

        self.assertEqual(decorated.name, enemy.name)
        self.assertEqual(decorated.health, enemy.health)
        self.assertEqual(
            decorated.max_health,
            enemy.max_health
        )


if __name__ == "__main__":
    unittest.main()
