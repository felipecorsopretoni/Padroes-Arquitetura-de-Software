from typing import Protocol

from src.strategies.registry import PaymentStrategyRegistry


class StatusUpdater(Protocol):
    def update_status(self, order_id: int, status: str) -> None:
        ...


class PaymentService:
    def __init__(
        self,
        status_updater: StatusUpdater,
        strategy_registry: PaymentStrategyRegistry,
    ) -> None:
        self._status_updater = status_updater
        self._strategy_registry = strategy_registry

    def process_payment(
        self,
        order_id: int,
        method: str,
        value: float,
        order_total: float,
    ) -> bool:
        strategy = self._strategy_registry.get(method)
        if strategy is None:
            print("Metodo de pagamento invalido!")
            return False

        required_amount = strategy.required_amount(order_total)
        if value < required_amount:
            print("Valor insuficiente!")
            return False

        processed = strategy.process(value, required_amount)
        if processed and strategy.auto_approve:
            self._status_updater.update_status(order_id, "aprovado")
        return processed
