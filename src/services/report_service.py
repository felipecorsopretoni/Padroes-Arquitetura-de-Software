from src.interfaces.order_repository_interface import OrderRepositoryInterface


class ReportService:
    def __init__(self, repository: OrderRepositoryInterface) -> None:
        self._repository = repository

    def calc_total_by_customer(self, name: str) -> float:
        orders = self._repository.get_orders_by_customer(name)
        return sum(order.total for order in orders)

    def generate(self, report_type: str) -> None:
        if report_type == "vendas":
            rows = self._repository.get_all_orders()
            print("=== RELATORIO DE VENDAS ===")
            total_amount = 0.0
            for order in rows:
                print(
                    f"Pedido #{order.order_id} - Cliente: {order.customer.name} - "
                    f"Total: R${order.total:.2f} - Status: {order.status}"
                )
                total_amount += order.total
            print(f"Total Geral: R${total_amount:.2f}")
            with open("rel_vendas.txt", "w", encoding="utf-8") as file_pointer:
                file_pointer.write(f"Total de vendas: {total_amount}")
            return

        if report_type == "clientes":
            rows = self._repository.get_distinct_customers()
            print("=== RELATORIO DE CLIENTES ===")
            for customer in rows:
                total_amount = self.calc_total_by_customer(customer.name)
                print(
                    f"Cliente: {customer.name} ({customer.customer_type}) - "
                    f"Total gasto: R${total_amount:.2f}"
                )
            with open("rel_clientes.txt", "w", encoding="utf-8") as file_pointer:
                for customer in rows:
                    file_pointer.write(f"{customer.name},{customer.customer_type}\n")
