from dataclasses import dataclass, field


@dataclass(frozen=True)
class Enchantment:
    name: str
    bonus_damage: int = 0
    bonus_defense: float = 0.0
    bonus_price: int = 0


SHARP = Enchantment(
    "Острое", bonus_damage=3, bonus_price=20
)

FIERY = Enchantment(
    "Огненное", bonus_damage=6, bonus_price=50
)

STURDY = Enchantment(
    "Прочное", bonus_defense=0.05, bonus_price=20
)

WARDING = Enchantment(
    "Охранное", bonus_defense=0.10, bonus_price=50
)


@dataclass
class Item:
    code: str
    name: str
    price: int
    enchantments: list[Enchantment] = field(
        default_factory=list
    )

    def copy(self) -> "Item":
        # У копии будет свой список зачарований.
        return Item(
            self.code,
            self.name,
            self.price,
            self.enchantments.copy()
        )

    def enchant(self, enchantment: Enchantment) -> None:
        if enchantment not in (
            SHARP, FIERY, STURDY, WARDING
        ):
            raise ValueError("Неизвестное зачарование")

        self.enchantments.append(enchantment)

    @property
    def damage_bonus(self) -> int:
        return sum(
            e.bonus_damage for e in self.enchantments
        )

    @property
    def defense(self) -> float:
        return min(
            0.75,
            sum(e.bonus_defense for e in self.enchantments)
        )

    def describe(self) -> str:
        names = (
            f" [{', '.join(e.name for e in self.enchantments)}]"
            if self.enchantments else ""
        )

        price = self.price + sum(
            e.bonus_price for e in self.enchantments
        )

        return (
            f"{self.name}{names} "
            f"(цена {price} золота)"
        )


class ItemCatalog:

    def __init__(self):
        self._prototypes = {
            "sword": Item(
                "sword", "Тренировочный меч", 20
            ),
            "bow": Item(
                "bow", "Охотничий лук", 20
            ),
            "staff": Item(
                "staff", "Посох ученика", 20
            ),
            "chainmail": Item(
                "chainmail", "Кольчуга", 40
            ),
            "leather": Item(
                "leather", "Кожаная броня", 30
            ),
            "robe": Item(
                "robe", "Льняная роба", 15
            ),
            "iron_sword": Item(
                "iron_sword", "Железный меч", 80
            ),
            "dragon_blade": Item(
                "dragon_blade", "Клинок дракона", 250
            ),
        }

    def create(self, code: str) -> Item:
        if code not in self._prototypes:
            raise ValueError(
                f"Предмет с кодом '{code}' не существует"
            )

        return self._prototypes[code].copy()