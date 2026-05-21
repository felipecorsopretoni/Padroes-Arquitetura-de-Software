from dataclasses import dataclass, replace
from typing import TypedDict

from src.models.customer import Customer
from src.models.order_item import LegacyItemPayload, OrderItem


class LegacyOrderPayload(TypedDict):
    id: int
    cli: str
    itens: list[LegacyItemPayload]
    tot: float
    st: str
    dt: str
    tp: str


@dataclass(frozen=True, slots=True)
class Order:
    customer: Customer
    items: tuple[OrderItem, ...]
    total: float
    status: str
    created_at: str
    order_id: int | None = None

    def with_id(self, order_id: int) -> "Order":
        return replace(self, order_id=order_id)

    def with_status(self, status: str) -> "Order":
        return replace(self, status=status)

    def with_customer_type(self, customer_type: str) -> "Order":
        return replace(
            self,
            customer=Customer(
                name=self.customer.name,
                customer_type=customer_type,
            ),
        )

    def to_legacy(self) -> LegacyOrderPayload:
        if self.order_id is None:
            raise ValueError("Order id must be defined before serialization")
        return {
            "id": self.order_id,
            "cli": self.customer.name,
            "itens": [item.to_legacy() for item in self.items],
            "tot": self.total,
            "st": self.status,
            "dt": self.created_at,
            "tp": self.customer.customer_type,
        }
