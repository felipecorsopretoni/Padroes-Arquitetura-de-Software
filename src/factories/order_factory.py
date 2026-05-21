from abc import ABC, abstractmethod
from typing import Sequence

from src.models.customer import Customer
from src.models.order import Order
from src.models.order_item import OrderItem


class OrderFactory(ABC):
    priority = 100

    @abstractmethod
    def supports(self, customer_type: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        raise NotImplementedError


class NormalOrderFactory(OrderFactory):
    priority = 10

    def supports(self, customer_type: str) -> bool:
        return customer_type == "normal"

    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        return Order(customer, tuple(items), total, "pendente", created_at)


class VipOrderFactory(OrderFactory):
    priority = 20

    def supports(self, customer_type: str) -> bool:
        return customer_type == "vip"

    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        return Order(customer, tuple(items), total, "pendente", created_at)


class CorporateOrderFactory(OrderFactory):
    priority = 30

    def supports(self, customer_type: str) -> bool:
        return customer_type == "corporativo"

    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        return Order(customer, tuple(items), total, "pendente", created_at)


class FallbackOrderFactory(OrderFactory):
    priority = 1000

    def supports(self, customer_type: str) -> bool:
        return True

    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        return Order(customer, tuple(items), total, "pendente", created_at)


class SpecialOrderFactory(OrderFactory):
    priority = 5

    def supports(self, customer_type: str) -> bool:
        return customer_type == "especial"

    def create(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        return Order(customer, tuple(items), total, "pendente", created_at)


class OrderFactoryRegistry:
    def __init__(self, factories: list[OrderFactory]):
        self._factories = factories

    def create_order(
        self,
        customer: Customer,
        items: Sequence[OrderItem],
        total: float,
        created_at: str,
    ) -> Order:
        for factory in self._factories:
            if factory.supports(customer.customer_type):
                return factory.create(customer, items, total, created_at)
        raise ValueError(f"No factory available for {customer.customer_type}")
