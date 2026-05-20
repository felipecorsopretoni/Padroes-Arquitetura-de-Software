class ReportService:
    def __init__(self, repository):
        self.repo = repository

    def calc_total_by_customer(self, name: str) -> float:
        orders = self.repo.get_orders_by_customer(name)
        return sum(row[3] for row in orders)

    def generate(self, report_type: str):
        if report_type == 'vendas':
            rows = self.repo.get_all_orders()
            print("=== RELATORIO DE VENDAS ===")
            tot_g = 0
            for r in rows:
                print(f"Pedido #{r[0]} - Cliente: {r[1]} - Total: R${r[3]:.2f} - Status: {r[4]}")
                tot_g += r[3]
            print(f"Total Geral: R${tot_g:.2f}")
            with open('rel_vendas.txt', 'w') as f:
                f.write(f"Total de vendas: {tot_g}")

        elif report_type == 'clientes':
            rows = self.repo.get_distinct_customers()
            print("=== RELATORIO DE CLIENTES ===")
            for r in rows:
                name, client_type = r[0], r[1]
                tot = self.calc_total_by_customer(name)
                print(f"Cliente: {name} ({client_type}) - Total gasto: R${tot:.2f}")
            with open('rel_clientes.txt', 'w') as f:
                for r in rows:
                    f.write(f"{r[0]},{r[1]}\n")