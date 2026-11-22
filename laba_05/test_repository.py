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
    """Структурный паттерн: Proxy (кэширование репозитория)."""

    def test_lazy_loading_and_single_storage_read(self):
        storage = Mock()

        heroes = [
            Mock(name="Артур"),
            Mock(name="Мерлин")
        ]

        storage.find_all.return_value = heroes

        cache = CachingHeroRepository(storage)

        storage.find_all.assert_not_called()

        first = cache.find_all()
        second = cache.find_all()

        storage.find_all.assert_called_once_with()

        self.assertEqual(first, second)

    def test_find_by_name(self):
        storage = Mock()

        hero = Mock()
        hero.name = "Артур"

        storage.find_by_name.return_value = hero

        cache = CachingHeroRepository(storage)

        result = cache.find_by_name("Артур")

        self.assertIs(result, hero)

        storage.find_by_name.assert_called_once_with(
            "Артур"
        )

    def test_save_delegates_to_storage(self):
        storage = Mock()
        cache = CachingHeroRepository(storage)

        hero = Mock()

        cache.save(hero)

        storage.save.assert_called_once_with(hero)


class TestFileHeroRepository(unittest.TestCase):
    """Интеграция: JSON-репозиторий и файловая система."""

    def test_save_creates_json_file(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "heroes.json"

            repository = FileHeroRepository(path)

            hero = Mock()
            hero.name = "Артур"

            repository.save(hero)

            self.assertTrue(path.is_file())

            with path.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            self.assertTrue(data)

    def test_missing_file_returns_empty_list(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "missing.json"

            repository = FileHeroRepository(path)

            self.assertEqual(
                repository.find_all(),
                []
            )


if __name__ == "__main__":
    unittest.main()
