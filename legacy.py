from src.repositories.order_repository import SQLiteOrderRepository
from src.services.notification_service import NotificationService
from src.services.order_service import OrderService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService

class Sis:
    def __init__(self):
        self.repository = SQLiteOrderRepository()
        self.notifier = NotificationService()
        self.order_service = OrderService(self.repository, self.notifier)
        self.payment_service = PaymentService(self.order_service)
        self.report_service = ReportService(self.repository)

    def add_ped(self, n, its, t):
        return self.order_service.create_order(n, its, t)

    def get_ped(self, id):
        return self.order_service.get_order(id)

    def upd_st(self, id, s):
        self.order_service.update_status(id, s)

    def calc_tot_cli(self, n):
        return self.report_service.calc_total_by_customer(n)

    def gerar_rel(self, tipo):
        self.report_service.generate(tipo)

    def proc_pag(self, id, m, vl):
    
        order = self.get_ped(id)
        if not order:
            print("Metodo de pagamento invalido!")  
            return False
            
        
        order_total = order['tot']
        return self.payment_service.process_payment(id, m, vl, order_total)

    def validar_estoque(self, its):
        return self.order_service.validate_stock(its)

    def cancelar_pedido(self, id):
        self.order_service.cancel_order(id)

    def close(self):
        self.repository.close()


class PedEspecial(Sis):
    # Mantida e adaptada temporariamente conforme as regras do EFC para manter compatibilidade no Sprint 1
    def add_ped(self, n, its, t):
        from datetime import datetime
        import json
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tot = 0
        for i in its:
            if i['tipo'] == 'normal':
                tot += i['p'] * i['q']
            elif i['tipo'] == 'desc10':
                tot += i['p'] * i['q'] * 0.9
            elif i['tipo'] == 'desc20':
                tot += i['p'] * i['q'] * 0.8
        tot = tot * 1.15
        its_str = json.dumps(its)
        
        order_id = self.repository.save(n, its_str, tot, t, dt)
        print(f"Email especial enviado para {n}: Pedido especial recebido!")
        return order_id

    def upd_st(self, id, s):
        self.repository.update_status(id, s)
        print(f"Pedido especial {id} -> {s}")