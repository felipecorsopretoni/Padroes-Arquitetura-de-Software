from dataclasses import dataclass

from src.discovery import discover_instances
from src.factories.order_factory import (
    CorporateOrderFactory,
    FallbackOrderFactory,
    NormalOrderFactory,
    OrderFactory,
    OrderFactoryRegistry,
    SpecialOrderFactory,
    VipOrderFactory,
)
from src.interfaces.order_repository_interface import OrderRepositoryInterface
from src.observers.base import NotificationObserver
from src.repositories.order_repository import SQLiteOrderRepository
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.pricing_service import PricingService
from src.services.report_service import ReportService
from src.services.special_order_service import SpecialOrderService
from src.strategies.base import (
    CustomerDiscountStrategy,
    ItemPricingStrategy,
    OrderAdjustmentStrategy,
    PaymentStrategy,
)
from src.strategies.registry import PaymentStrategyRegistry


@dataclass(slots=True)
class AppContainer:
    repository: OrderRepositoryInterface
    order_service: OrderService
    payment_service: PaymentService
    report_service: ReportService


@dataclass(slots=True)
class SpecialAppContainer:
    repository: OrderRepositoryInterface
    order_service: SpecialOrderService


def _build_pricing_service() -> PricingService:
    return PricingService(
        item_strategies=discover_instances("src.strategies", ItemPricingStrategy),
        customer_strategies=discover_instances(
            "src.strategies",
            CustomerDiscountStrategy,
        ),
        order_adjustments=discover_instances(
            "src.strategies",
            OrderAdjustmentStrategy,
        ),
    )


def _build_order_factories() -> list[OrderFactory]:
    return [
        NormalOrderFactory(),
        VipOrderFactory(),
        CorporateOrderFactory(),
        FallbackOrderFactory(),
    ]


def build_app_container(db_path: str = "loja.db") -> AppContainer:
    repository = SQLiteOrderRepository(db_path)
    notification_service = NotificationService(
        discover_instances("src.observers", NotificationObserver)
    )
    pricing_service = _build_pricing_service()
    order_service = OrderService(
        repository=repository,
        notification_service=notification_service,
        pricing_service=pricing_service,
        factory_registry=OrderFactoryRegistry(_build_order_factories()),
    )
    payment_service = PaymentService(
        status_updater=order_service,
        strategy_registry=PaymentStrategyRegistry(
            discover_instances("src.strategies", PaymentStrategy)
        ),
    )
    report_service = ReportService(repository)
    return AppContainer(
        repository=repository,
        order_service=order_service,
        payment_service=payment_service,
        report_service=report_service,
    )


def build_special_app_container(db_path: str = "loja.db") -> SpecialAppContainer:
    repository = SQLiteOrderRepository(db_path)
    pricing_service = _build_pricing_service()
    order_service = SpecialOrderService(
        repository=repository,
        pricing_service=pricing_service,
        order_factory=SpecialOrderFactory(),
    )
    return SpecialAppContainer(repository=repository, order_service=order_service)
