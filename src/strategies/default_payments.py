from src.strategies.base import PaymentStrategy


class CardPaymentStrategy(PaymentStrategy):
    priority = 10
    method_name = "cartao"
    auto_approve = True

    def supports(self, method: str) -> bool:
        return method == self.method_name

    def process(self, paid_amount: float, required_amount: float) -> bool:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return True


class PixPaymentStrategy(PaymentStrategy):
    priority = 20
    method_name = "pix"
    auto_approve = True

    def supports(self, method: str) -> bool:
        return method == self.method_name

    def process(self, paid_amount: float, required_amount: float) -> bool:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return True


class BoletoPaymentStrategy(PaymentStrategy):
    priority = 30
    method_name = "boleto"
    auto_approve = False

    def supports(self, method: str) -> bool:
        return method == self.method_name

    def process(self, paid_amount: float, required_amount: float) -> bool:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return True
