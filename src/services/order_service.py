import json
from datetime import datetime

class OrderService:
    def __init__(self, repository, notification_service):
        self.repo = repository
        self.notifier = notification_service

    def validate_stock(self, items: list) -> bool:
        stock = {'produto1': 100, 'produto2': 50, 'produto3': 75}
        for i in items:
            if i['nome'] not in stock:
                print(f"Produto {i['nome']} nao encontrado!")
                return False
            if stock[i['nome']] < i['q']:
                print(f"Estoque insuficiente para {i['nome']}!")
                return False
        return True

    def calculate_total(self, items: list, client_type: str) -> float:
        total = 0
        for i in items:
            if i['tipo'] == 'normal':
                total += i['p'] * i['q']
            elif i['tipo'] == 'desc10':
                total += i['p'] * i['q'] * 0.9
            elif i['tipo'] == 'desc20':
                total += i['p'] * i['q'] * 0.8
            elif i['tipo'] == 'frete_gratis':
                total += i['p'] * i['q']

        if client_type == 'vip':
            total *= 0.95
        elif client_type == 'corporativo':
            total *= 0.90
        return total

    def create_order(self, name: str, items: list, client_type: str) -> int:
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total = self.calculate_total(items, client_type)
        items_json = json.dumps(items)
        
        order_id = self.repo.save(name, items_json, total, client_type, date_str)
        self.notifier.notify_order_received(name, client_type)
        return order_id

    def get_order(self, order_id: int) -> dict:
        r = self.repo.get_by_id(order_id)
        if r:
            return {'id': r[0], 'cli': r[1], 'itens': json.loads(r[2]),
                    'tot': r[3], 'st': r[4], 'dt': r[5], 'tp': r[6]}
        return None

    def update_status(self, order_id: int, status: str):
        order = self.get_order(order_id)
        if order:
            self.repo.update_status(order_id, status)
            self.notifier.notify_status_changed(order['cli'], status, order['tp'])
            if status == 'entregue':
                self.notifier.notify_loyalty_points(order['tp'], order['tot'])

    def cancel_order(self, order_id: int):
        self.repo.update_status(order_id, 'cancelado')
        print(f"Pedido {order_id} cancelado")