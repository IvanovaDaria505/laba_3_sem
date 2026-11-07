import json
from pathlib import Path

class FileHeroRepository:
    def __init__(self, path):
        self.path = Path(path)

    def find_all(self):
        if not self.path.exists():
            return []
        raw = self.path.read_text(encoding="utf-8").strip()
        return json.loads(raw) if raw else []

    def find_by_name(self, name):
        for data in self.find_all():
            if data["name"] == name:
                return dict(data)
        return None

    def save(self, hero_data):
        heroes = [h for h in self.find_all() if h["name"] != hero_data["name"]]
        heroes.append(hero_data)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(heroes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

class CachingHeroRepository:
    def __init__(self, target):
        self.target = target
        self.cache = None

    def _cached(self):
        if self.cache is None:
            self.cache = {hero["name"]: hero for hero in self.target.find_all()}
        return self.cache

    def find_by_name(self, name):
        return self._cached().get(name)

    def find_all(self):
        return list(self._cached().values())

    def save(self, hero_data):
        self.target.save(hero_data)
        self._cached()[hero_data["name"]] = hero_data
