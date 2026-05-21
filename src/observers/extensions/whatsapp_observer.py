from src.models.order import Order
from src.observers.base import NotificationObserver


class WhatsAppObserver(NotificationObserver):
    priority = 15

    def supports(self, customer_type: str) -> bool:
        return True

    def on_order_received(self, order: Order) -> None:
        print(f"WhatsApp enviado para {order.customer.name}: Pedido recebido!")

    def on_status_changed(self, order: Order, status: str) -> None:
        if status == "aprovado":
            print(f"WhatsApp enviado para {order.customer.name}: Pedido aprovado!")
        elif status == "enviado":
            print(f"WhatsApp enviado para {order.customer.name}: Pedido enviado!")
        elif status == "entregue":
            print(f"WhatsApp enviado para {order.customer.name}: Pedido entregue!")
