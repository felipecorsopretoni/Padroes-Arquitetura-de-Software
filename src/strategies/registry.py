from src.strategies.base import PaymentStrategy


class PaymentStrategyRegistry:
    def __init__(self, strategies: list[PaymentStrategy]):
        self._strategies = strategies

    def get(self, method: str) -> PaymentStrategy | None:
        for strategy in self._strategies:
            if strategy.supports(method):
                return strategy
        return None
