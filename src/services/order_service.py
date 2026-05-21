from datetime import datetime

from src.factories.order_factory import OrderFactoryRegistry
from src.interfaces.order_repository_interface import OrderRepositoryInterface
from src.models.customer import Customer
from src.models.order import LegacyOrderPayload, Order
from src.models.order_item import LegacyItemPayload, OrderItem
from src.services.notification_service import NotificationService
from src.services.pricing_service import PricingService


class OrderService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        notification_service: NotificationService,
        pricing_service: PricingService,
        factory_registry: OrderFactoryRegistry,
    ) -> None:
        self._repository = repository
        self._notification_service = notification_service
        self._pricing_service = pricing_service
        self._factory_registry = factory_registry

    def validate_stock(self, items: list[LegacyItemPayload]) -> bool:
        stock = {"produto1": 100, "produto2": 50, "produto3": 75}
        for item in items:
            if item["nome"] not in stock:
                print(f"Produto {item['nome']} nao encontrado!")
                return False
            if stock[item["nome"]] < item["q"]:
                print(f"Estoque insuficiente para {item['nome']}!")
                return False
        return True

    def create_order(
        self,
        name: str,
        items_payload: list[LegacyItemPayload],
        client_type: str,
    ) -> int:
        customer = Customer(name=name, customer_type=client_type)
        items = tuple(OrderItem.from_legacy(item) for item in items_payload)
        total = self._pricing_service.calculate_total(items, client_type)
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        order = self._factory_registry.create_order(customer, items, total, date_str)
        order_id = self._repository.save(order)
        persisted = self.get_order_entity(order_id)
        if persisted is None:
            raise ValueError(f"Order {order_id} was not persisted correctly")
        self._notification_service.notify_order_received(persisted)
        return order_id

    def get_order(self, order_id: int) -> LegacyOrderPayload | None:
        order = self._repository.get_by_id(order_id)
        if order is not None:
            return order.to_legacy()
        return None

    def get_order_entity(self, order_id: int) -> Order | None:
        return self._repository.get_by_id(order_id)

    def update_status(self, order_id: int, status: str) -> None:
        order = self._repository.get_by_id(order_id)
        if order is not None:
            self._repository.update_status(order_id, status)
            self._notification_service.notify_status_changed(
                order.with_status(status),
                status,
            )

    def cancel_order(self, order_id: int) -> None:
        self._repository.update_status(order_id, "cancelado")
        print(f"Pedido {order_id} cancelado")
