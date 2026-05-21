from typing import Sequence

from src.models.order_item import OrderItem
from src.strategies.base import (
    CustomerDiscountStrategy,
    ItemPricingStrategy,
    OrderAdjustmentStrategy,
)


class NormalItemPricingStrategy(ItemPricingStrategy):
    priority = 10

    def supports(self, item: OrderItem) -> bool:
        return item.item_type == "normal"

    def calculate(self, item: OrderItem) -> float:
        return item.price * item.quantity


class Discount10ItemPricingStrategy(ItemPricingStrategy):
    priority = 20

    def supports(self, item: OrderItem) -> bool:
        return item.item_type == "desc10"

    def calculate(self, item: OrderItem) -> float:
        return item.price * item.quantity * 0.9


class Discount20ItemPricingStrategy(ItemPricingStrategy):
    priority = 30

    def supports(self, item: OrderItem) -> bool:
        return item.item_type == "desc20"

    def calculate(self, item: OrderItem) -> float:
        return item.price * item.quantity * 0.8


class FreeShippingItemPricingStrategy(ItemPricingStrategy):
    priority = 40

    def supports(self, item: OrderItem) -> bool:
        return item.item_type == "frete_gratis"

    def calculate(self, item: OrderItem) -> float:
        return item.price * item.quantity


class DefaultCustomerDiscountStrategy(CustomerDiscountStrategy):
    priority = 1000

    def supports(self, customer_type: str) -> bool:
        return True

    def apply(self, current_total: float) -> float:
        return current_total


class VipCustomerDiscountStrategy(CustomerDiscountStrategy):
    priority = 10

    def supports(self, customer_type: str) -> bool:
        return customer_type == "vip"

    def apply(self, current_total: float) -> float:
        return current_total * 0.95


class CorporateCustomerDiscountStrategy(CustomerDiscountStrategy):
    priority = 20

    def supports(self, customer_type: str) -> bool:
        return customer_type == "corporativo"

    def apply(self, current_total: float) -> float:
        return current_total * 0.90


class NoOpOrderAdjustmentStrategy(OrderAdjustmentStrategy):
    priority = 1000

    def apply(self, items: Sequence[OrderItem], current_total: float) -> float:
        return current_total
