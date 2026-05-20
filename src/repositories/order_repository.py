import sqlite3
from src.interfaces.order_repository_interface import OrderRepositoryInterface

class SQLiteOrderRepository(OrderRepositoryInterface):
    def __init__(self, db_path='loja.db'):
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS ped (
            id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
            tot REAL, st TEXT, dt TEXT, tp TEXT)''')
        self.db.commit()

    def save(self, client_name: str, items_str: str, total: float, client_type: str, date_str: str) -> int:
        self.c.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (client_name, items_str, total, 'pendente', date_str, client_type))
        self.db.commit()
        return self.c.lastrowid

    def get_by_id(self, order_id: int) -> tuple:
        self.c.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        return self.c.fetchone()

    def update_status(self, order_id: int, status: str) -> None:
        self.c.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self.db.commit()

    def get_all_orders(self) -> list:
        self.c.execute("SELECT * FROM ped")
        return self.c.fetchall()

    def get_distinct_customers(self) -> list:
        self.c.execute("SELECT DISTINCT cli, tp FROM ped")
        return self.c.fetchall()

    def get_orders_by_customer(self, customer_name: str) -> list:
        self.c.execute("SELECT * FROM ped WHERE cli=?", (customer_name,))
        return self.c.fetchall()

    def close(self):
        self.db.close()