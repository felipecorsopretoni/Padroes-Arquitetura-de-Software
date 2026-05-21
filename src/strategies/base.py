from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import ClassVar

from src.models.order_item import OrderItem


class ItemPricingStrategy(ABC):
    priority = 100

    @abstractmethod
    def supports(self, item: OrderItem) -> bool:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, item: OrderItem) -> float:
        raise NotImplementedError


class OrderAdjustmentStrategy(ABC):
    priority = 100

    @abstractmethod
    def apply(self, items: Sequence[OrderItem], current_total: float) -> float:
        raise NotImplementedError


class CustomerDiscountStrategy(ABC):
    priority = 100

    @abstractmethod
    def supports(self, customer_type: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def apply(self, current_total: float) -> float:
        raise NotImplementedError


class PaymentStrategy(ABC):
    priority = 100
    method_name: ClassVar[str]
    auto_approve = False

    @abstractmethod
    def supports(self, method: str) -> bool:
        raise NotImplementedError

    def required_amount(self, order_total: float) -> float:
        return order_total

    @abstractmethod
    def process(self, paid_amount: float, required_amount: float) -> bool:
        raise NotImplementedError
