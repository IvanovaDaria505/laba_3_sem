import unittest
import json

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock

from repository import (
    FileHeroRepository,
    CachingHeroRepository
)

class TestCachingHeroRepository(unittest.TestCase):

    def test_lazy_loading_and_single_storage_read(self):
        heroes = [
            {"name": "Артур", "level": 5},
            {"name": "Мерлин", "level": 10}
        ]

        storage = Mock()
        storage.find_all.return_value = heroes

        cache = CachingHeroRepository(storage)

        storage.find_all.assert_not_called()

        first = cache.find_all()
        second = cache.find_all()

        storage.find_all.assert_called_once_with()

        self.assertEqual(first, second)
        self.assertEqual(len(first), 2)

    def test_find_by_name(self):
        heroes = [
            {"name": "Артур", "level": 5},
            {"name": "Мерлин", "level": 10}
        ]

        storage = Mock()
        storage.find_all.return_value = heroes

        cache = CachingHeroRepository(storage)

        result = cache.find_by_name("Артур")

        self.assertEqual(result["name"], "Артур")
        self.assertEqual(result["level"], 5)

    def test_save_delegates_to_storage(self):
        storage = Mock()
        storage.find_all.return_value = []

        cache = CachingHeroRepository(storage)

        hero = {"name": "Артур", "level": 5}

        cache.save(hero)

        storage.save.assert_called_once_with(hero)

        self.assertEqual(
            cache.find_by_name("Артур"),
            hero
        )

class TestFileHeroRepository(unittest.TestCase):

    def test_save_creates_json_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "heroes.json"

            repository = FileHeroRepository(path)

            hero = {
                "name": "Артур",
                "level": 5
            }

            repository.save(hero)

            self.assertTrue(path.is_file())

            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data, [hero])

    def test_missing_file_returns_empty_list(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            repository = FileHeroRepository(path)

            self.assertEqual(repository.find_all(), [])

if __name__ == "__main__":
    unittest.main()
