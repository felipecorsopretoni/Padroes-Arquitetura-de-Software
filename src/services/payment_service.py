class PaymentService:
    def __init__(self, order_service):
        self.order_service = order_service

    def process_payment(self, order_id: int, method: str, value: float, order_total: float) -> bool:
        if value < order_total:
            print("Valor insuficiente!")
            return False
        
        if method == 'cartao':
            print("Processando pagamento com cartao...")
            print("Cartao validado!")
            self.order_service.update_status(order_id, 'aprovado')
            return True
        elif method == 'pix':
            print("Gerando QR Code PIX...")
            print("PIX recebido!")
            self.order_service.update_status(order_id, 'aprovado')
            return True
        elif method == 'boleto':
            print("Gerando boleto...")
            print("Boleto gerado!")
            return True
        else:
            print("Metodo de pagamento invalido!")
            return False