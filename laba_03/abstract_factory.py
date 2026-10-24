from abc import ABC, abstractmethod
from prototype import Item, ItemCatalog


class StarterKitFactory(ABC):

    @abstractmethod
    def create_weapon(self) -> Item:
        pass

    @abstractmethod
    def create_armor(self) -> Item:
        pass


class WarriorKitFactory(StarterKitFactory):

    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Item:
        return self.catalog.create("sword")

    def create_armor(self) -> Item:
        return self.catalog.create("chainmail")


class RangerKitFactory(StarterKitFactory):

    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Item:
        return self.catalog.create("bow")

    def create_armor(self) -> Item:
        return self.catalog.create("leather")


class MageKitFactory(StarterKitFactory):

    def __init__(self, catalog: ItemCatalog):
        self.catalog = catalog

    def create_weapon(self) -> Item:
        return self.catalog.create("staff")

    def create_armor(self) -> Item:
        return self.catalog.create("robe")