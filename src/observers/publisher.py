from collections.abc import Iterable

from src.models.order import Order
from src.observers.base import NotificationObserver


class NotificationPublisher:
    def __init__(self, observers: Iterable[NotificationObserver]):
        self._observers = list(observers)

    def publish_order_received(self, order: Order) -> None:
        for observer in self._observers:
            if observer.supports(order.customer.customer_type):
                observer.on_order_received(order)

    def publish_status_changed(self, order: Order, status: str) -> None:
        for observer in self._observers:
            if observer.supports(order.customer.customer_type):
                observer.on_status_changed(order, status)
