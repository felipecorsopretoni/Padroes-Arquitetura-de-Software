from src.strategies.base import PaymentStrategy


class CryptoPaymentStrategy(PaymentStrategy):
    priority = 25
    method_name = "criptomoeda"
    auto_approve = True

    def supports(self, method: str) -> bool:
        return method == self.method_name

    def required_amount(self, order_total: float) -> float:
        return order_total * 1.02

    def process(self, paid_amount: float, required_amount: float) -> bool:
        print("Processando pagamento em criptomoeda...")
        print("Pagamento em criptomoeda confirmado!")
        return True
