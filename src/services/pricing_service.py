from collections.abc import Sequence

from src.models.order_item import OrderItem
from src.strategies.base import (
    CustomerDiscountStrategy,
    ItemPricingStrategy,
    OrderAdjustmentStrategy,
)


class PricingService:
    def __init__(
        self,
        item_strategies: Sequence[ItemPricingStrategy],
        customer_strategies: Sequence[CustomerDiscountStrategy],
        order_adjustments: Sequence[OrderAdjustmentStrategy],
    ) -> None:
        self._item_strategies = list(item_strategies)
        self._customer_strategies = list(customer_strategies)
        self._order_adjustments = list(order_adjustments)

    def calculate_items_total(self, items: Sequence[OrderItem]) -> float:
        total = 0.0
        for item in items:
            total += self._calculate_item_total(item)
        return total

    def calculate_total(
        self,
        items: Sequence[OrderItem],
        customer_type: str,
    ) -> float:
        total = self.calculate_items_total(items)
        for adjustment in self._order_adjustments:
            total = adjustment.apply(items, total)
        return self._apply_customer_discount(customer_type, total)

    def _calculate_item_total(self, item: OrderItem) -> float:
        for strategy in self._item_strategies:
            if strategy.supports(item):
                return strategy.calculate(item)
        raise ValueError(f"Unsupported item type: {item.item_type}")

    def _apply_customer_discount(self, customer_type: str, total: float) -> float:
        for strategy in self._customer_strategies:
            if strategy.supports(customer_type):
                return strategy.apply(total)
        return total
