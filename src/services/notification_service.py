from collections.abc import Iterable

from src.models.order import Order
from src.observers.base import NotificationObserver
from src.observers.publisher import NotificationPublisher


class NotificationService:
    def __init__(self, observers: Iterable[NotificationObserver]) -> None:
        self._publisher = NotificationPublisher(observers)

    def notify_order_received(self, order: Order) -> None:
        self._publisher.publish_order_received(order)

    def notify_status_changed(self, order: Order, status: str) -> None:
        self._publisher.publish_status_changed(order, status)
