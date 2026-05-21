import json
import sqlite3

from src.interfaces.order_repository_interface import OrderRepositoryInterface
from src.models.customer import Customer
from src.models.order import Order
from src.models.order_item import LegacyItemPayload, OrderItem


class SQLiteOrderRepository(OrderRepositoryInterface):
    def __init__(self, db_path: str = "loja.db") -> None:
        self._db = sqlite3.connect(db_path)
        self._cursor = self._db.cursor()
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS ped (
            id INTEGER PRIMARY KEY, cli TEXT, itens TEXT,
            tot REAL, st TEXT, dt TEXT, tp TEXT)"""
        )
        self._db.commit()

    def save(self, order: Order) -> int:
        items_json = json.dumps([item.to_legacy() for item in order.items])
        self._cursor.execute(
            "INSERT INTO ped (cli, itens, tot, st, dt, tp) VALUES (?, ?, ?, ?, ?, ?)",
            (
                order.customer.name,
                items_json,
                order.total,
                order.status,
                order.created_at,
                order.customer.customer_type,
            ),
        )
        self._db.commit()
        return int(self._cursor.lastrowid)

    def get_by_id(self, order_id: int) -> Order | None:
        self._cursor.execute("SELECT * FROM ped WHERE id=?", (order_id,))
        row = self._cursor.fetchone()
        if row is None:
            return None
        return self._row_to_order(row)

    def update_status(self, order_id: int, status: str) -> None:
        self._cursor.execute("UPDATE ped SET st=? WHERE id=?", (status, order_id))
        self._db.commit()

    def get_all_orders(self) -> list[Order]:
        self._cursor.execute("SELECT * FROM ped")
        return [self._row_to_order(row) for row in self._cursor.fetchall()]

    def get_distinct_customers(self) -> list[Customer]:
        self._cursor.execute("SELECT DISTINCT cli, tp FROM ped")
        return [Customer(name=row[0], customer_type=row[1]) for row in self._cursor.fetchall()]

    def get_orders_by_customer(self, customer_name: str) -> list[Order]:
        self._cursor.execute("SELECT * FROM ped WHERE cli=?", (customer_name,))
        return [self._row_to_order(row) for row in self._cursor.fetchall()]

    def close(self) -> None:
        self._db.close()

    def _row_to_order(self, row: tuple[object, ...]) -> Order:
        raw_items = json.loads(str(row[2]))
        payload_items = [self._normalize_item(item) for item in raw_items]
        return Order(
            customer=Customer(name=str(row[1]), customer_type=str(row[6])),
            items=tuple(OrderItem.from_legacy(item) for item in payload_items),
            total=float(row[3]),
            status=str(row[4]),
            created_at=str(row[5]),
            order_id=int(row[0]),
        )

    def _normalize_item(self, raw_item: object) -> LegacyItemPayload:
        if not isinstance(raw_item, dict):
            raise ValueError("Stored item must be a dictionary")
        return {
            "nome": str(raw_item["nome"]),
            "p": float(raw_item["p"]),
            "q": int(raw_item["q"]),
            "tipo": str(raw_item["tipo"]),
        }
