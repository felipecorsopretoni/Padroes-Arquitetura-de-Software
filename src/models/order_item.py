from dataclasses import dataclass
from typing import TypedDict


class LegacyItemPayload(TypedDict):
    nome: str
    p: float
    q: int
    tipo: str


@dataclass(frozen=True, slots=True)
class OrderItem:
    name: str
    price: float
    quantity: int
    item_type: str

    @classmethod
    def from_legacy(cls, payload: LegacyItemPayload) -> "OrderItem":
        return cls(
            name=payload["nome"],
            price=float(payload["p"]),
            quantity=int(payload["q"]),
            item_type=payload["tipo"],
        )

    def to_legacy(self) -> LegacyItemPayload:
        return {
            "nome": self.name,
            "p": self.price,
            "q": self.quantity,
            "tipo": self.item_type,
        }
