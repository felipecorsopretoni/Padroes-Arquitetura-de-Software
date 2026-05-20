class NotificationService:
    def notify_order_received(self, name: str, client_type: str):
        print(f"Email enviado para {name}: Pedido recebido!")
        if client_type == 'vip':
            print(f"SMS enviado para {name}: Pedido VIP recebido!")
        elif client_type == 'corporativo':
            print(f"Notificacao enviada ao gerente de conta de {name}")

    def notify_status_changed(self, name: str, status: str, client_type: str):
        if status == 'aprovado':
            print(f"Email enviado para {name}: Pedido aprovado!")
            if client_type == 'vip':
                print(f"SMS enviado para {name}: Pedido aprovado!")
        elif status == 'enviado':
            print(f"Email enviado para {name}: Pedido enviado!")
        elif status == 'entregue':
            print(f"Email enviado para {name}: Pedido entregue!")

    def notify_loyalty_points(self, client_type: str, total: float):
        if client_type == 'vip':
            pts = int(total * 2)
            print(f"Cliente VIP ganhou {pts} pontos!")
        elif client_type == 'corporativo':
            pts = int(total * 1.5)
            print(f"Cliente corporativo ganhou {pts} pontos!")
        else:
            pts = int(total)
            print(f"Cliente ganhou {pts} pontos!")