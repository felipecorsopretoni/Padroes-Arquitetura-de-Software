from src.models.order import Order
from src.observers.base import NotificationObserver


class EmailObserver(NotificationObserver):
    priority = 10

    def supports(self, customer_type: str) -> bool:
        return True

    def on_order_received(self, order: Order) -> None:
        print(f"Email enviado para {order.customer.name}: Pedido recebido!")

    def on_status_changed(self, order: Order, status: str) -> None:
        if status == "aprovado":
            print(f"Email enviado para {order.customer.name}: Pedido aprovado!")
        elif status == "enviado":
            print(f"Email enviado para {order.customer.name}: Pedido enviado!")
        elif status == "entregue":
            print(f"Email enviado para {order.customer.name}: Pedido entregue!")


class SmsObserver(NotificationObserver):
    priority = 20

    def supports(self, customer_type: str) -> bool:
        return customer_type == "vip"

    def on_order_received(self, order: Order) -> None:
        print(f"SMS enviado para {order.customer.name}: Pedido VIP recebido!")

    def on_status_changed(self, order: Order, status: str) -> None:
        if status == "aprovado":
            print(f"SMS enviado para {order.customer.name}: Pedido aprovado!")


class AccountManagerObserver(NotificationObserver):
    priority = 30

    def supports(self, customer_type: str) -> bool:
        return customer_type == "corporativo"

    def on_order_received(self, order: Order) -> None:
        print(f"Notificacao enviada ao gerente de conta de {order.customer.name}")


class LoyaltyPointsObserver(NotificationObserver):
    priority = 40

    def supports(self, customer_type: str) -> bool:
        return True

    def on_status_changed(self, order: Order, status: str) -> None:
        if status != "entregue":
            return
        if order.customer.customer_type == "vip":
            points = int(order.total * 2)
            print(f"Cliente VIP ganhou {points} pontos!")
        elif order.customer.customer_type == "corporativo":
            points = int(order.total * 1.5)
            print(f"Cliente corporativo ganhou {points} pontos!")
        else:
            points = int(order.total)
            print(f"Cliente ganhou {points} pontos!")
