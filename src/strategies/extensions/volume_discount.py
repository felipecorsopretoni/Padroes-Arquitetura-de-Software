from collections import Counter
from collections.abc import Sequence

from src.models.order_item import OrderItem
from src.strategies.base import OrderAdjustmentStrategy


class VolumeDiscountStrategy(OrderAdjustmentStrategy):
    priority = 10

    def apply(self, items: Sequence[OrderItem], current_total: float) -> float:
        quantities = Counter(item.name for item in items for _ in range(item.quantity))
        discount = 0.0
        for item in items:
            if quantities[item.name] >= 3:
                discount += item.price * item.quantity * 0.15
        return current_total - discount
