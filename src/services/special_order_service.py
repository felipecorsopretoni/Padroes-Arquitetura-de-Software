from datetime import datetime

from src.factories.order_factory import SpecialOrderFactory
from src.interfaces.order_repository_interface import OrderRepositoryInterface
from src.models.customer import Customer
from src.models.order import LegacyOrderPayload
from src.models.order_item import LegacyItemPayload, OrderItem
from src.services.pricing_service import PricingService


class SpecialOrderService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        pricing_service: PricingService,
        order_factory: SpecialOrderFactory,
    ) -> None:
        self._repository = repository
        self._pricing_service = pricing_service
        self._order_factory = order_factory

    def create_order(
        self,
        name: str,
        items_payload: list[LegacyItemPayload],
        customer_type: str,
    ) -> int:
        customer = Customer(name=name, customer_type=customer_type)
        items = tuple(OrderItem.from_legacy(item) for item in items_payload)
        total = self._pricing_service.calculate_items_total(items) * 1.15
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        order = self._order_factory.create(
            Customer(name=customer.name, customer_type="especial"),
            items,
            total,
            created_at,
        )
        order_id = self._repository.save(order)
        print(f"Email especial enviado para {name}: Pedido especial recebido!")
        return order_id

    def get_order(self, order_id: int) -> LegacyOrderPayload | None:
        order = self._repository.get_by_id(order_id)
        if order is None:
            return None
        return order.with_customer_type("normal").to_legacy()

    def update_status(self, order_id: int, status: str) -> None:
        self._repository.update_status(order_id, status)
        print(f"Pedido especial {order_id} -> {status}")
