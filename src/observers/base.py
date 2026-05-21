from abc import ABC, abstractmethod

from src.models.order import Order


class NotificationObserver(ABC):
    priority = 100

    @abstractmethod
    def supports(self, customer_type: str) -> bool:
        raise NotImplementedError

    def on_order_received(self, order: Order) -> None:
        return None

    def on_status_changed(self, order: Order, status: str) -> None:
        return None
