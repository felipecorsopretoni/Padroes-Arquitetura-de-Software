from abc import ABC, abstractmethod

from src.models.customer import Customer
from src.models.order import Order


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    def get_distinct_customers(self) -> list[Customer]:
        raise NotImplementedError

    @abstractmethod
    def get_orders_by_customer(self, customer_name: str) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
