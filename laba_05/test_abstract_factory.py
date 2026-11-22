import unittest

from abstract_factory import (
    WarriorKitFactory,
    RangerKitFactory,
    MageKitFactory
)
from prototype import ItemCatalog, FIERY

class TestAbstractFactory(unittest.TestCase):
    """Порождающий паттерн: Абстрактная фабрика."""

    def setUp(self):
        self.catalog = ItemCatalog()

    def test_warrior_factory(self):
        factory = WarriorKitFactory(self.catalog)

        weapon = factory.create_weapon()
        armor = factory.create_armor()

        self.assertEqual(weapon.code, "sword")
        self.assertEqual(armor.code, "chainmail")

    def test_ranger_factory(self):
        factory = RangerKitFactory(self.catalog)

        weapon = factory.create_weapon()
        armor = factory.create_armor()

        self.assertEqual(weapon.code, "bow")
        self.assertEqual(armor.code, "leather")

    def test_mage_factory(self):
        factory = MageKitFactory(self.catalog)

        weapon = factory.create_weapon()
        armor = factory.create_armor()

        self.assertEqual(weapon.code, "staff")
        self.assertEqual(armor.code, "robe")

    def test_created_items_are_independent(self):
        factory = WarriorKitFactory(self.catalog)

        first = factory.create_weapon()
        second = factory.create_weapon()

        self.assertIsNot(first, second)

        first.enchant(FIERY)

        self.assertEqual(len(first.enchantments), 1)
        self.assertEqual(len(second.enchantments), 0)

    def test_factory_uses_catalog(self):
        factory = WarriorKitFactory(self.catalog)

        weapon = factory.create_weapon()

        self.assertEqual(
            weapon.name,
            "Тренировочный меч"
        )

if __name__ == "__main__":
    unittest.main()
