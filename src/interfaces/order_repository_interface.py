from abc import ABC, abstractmethod

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, client_name: str, items_str: str, total: float, client_type: str, date_str: str) -> int:
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> tuple:
        pass

    @abstractmethod
    def update_status(self, order_id: int, status: str) -> None:
        pass

    @abstractmethod
    def get_all_orders(self) -> list:
        pass

    @abstractmethod
    def get_distinct_customers(self) -> list:
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_name: str) -> list:
        pass