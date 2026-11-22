import unittest
from unittest.mock import Mock

from chain import (
    ArmorHandler,
    BarrierHandler,
    EvasionHandler
)
from damage import Damage


class TestDefense(unittest.TestCase):
    """Поведенческий паттерн: Цепочка обязанностей."""

    def test_armor_boundaries(self):
        for incoming, absorbed, remaining in (
            (0, 0, 0),
            (10, 3, 7),
            (30, 9, 21),
            (100, 30, 70)
        ):
            with self.subTest(incoming=incoming):
                damage = Damage(incoming)

                ArmorHandler(0.3).handle(damage)

                self.assertEqual(
                    damage.absorbed,
                    absorbed
                )
                self.assertEqual(
                    damage.amount,
                    remaining
                )
                self.assertFalse(damage.evaded)

    def test_barrier_boundaries(self):
        for incoming, absorbed, remaining, points in (
            (0, 0, 0, 30),
            (10, 10, 0, 20),
            (30, 30, 0, 0),
            (40, 30, 10, 0)
        ):
            with self.subTest(incoming=incoming):
                barrier = BarrierHandler(30)
                damage = Damage(incoming)

                barrier.handle(damage)

                self.assertEqual(
                    damage.absorbed,
                    absorbed
                )
                self.assertEqual(
                    damage.amount,
                    remaining
                )
                self.assertEqual(
                    barrier.points,
                    points
                )

    def test_damage_passes_through_multiple_handlers(self):
        armor = ArmorHandler(0.3)
        barrier = BarrierHandler(20)

        armor.set_next(barrier)

        damage = Damage(100)
        result = armor.handle(damage)

        self.assertIs(result, damage)
        self.assertEqual(damage.absorbed, 50)
        self.assertEqual(damage.amount, 50)
        self.assertEqual(barrier.points, 0)

    def test_successful_evasion_stops_chain(self):
        rng = Mock()
        rng.random.return_value = 0.1

        following = Mock()

        evasion = EvasionHandler(
            0.5,
            rng=rng
        )
        evasion.set_next(following)

        damage = Damage(20)
        result = evasion.handle(damage)

        self.assertIs(result, damage)
        self.assertTrue(damage.evaded)
        self.assertEqual(damage.amount, 0)

        rng.random.assert_called_once()
        following.handle.assert_not_called()

    def test_failed_evasion_forwards_damage(self):
        rng = Mock()
        rng.random.return_value = 0.9

        following = Mock()

        evasion = EvasionHandler(
            0.5,
            rng=rng
        )
        evasion.set_next(following)

        damage = Damage(20)
        result = evasion.handle(damage)

        self.assertIs(result, damage)
        self.assertFalse(damage.evaded)

        following.handle.assert_called_once_with(damage)


if __name__ == "__main__":
    unittest.main()
