from src.main import build_app_container, build_special_app_container
from src.models.order import LegacyOrderPayload
from src.models.order_item import LegacyItemPayload

class Sis:
    def __init__(self, db_path: str = "loja.db") -> None:
        container = build_app_container(db_path)
        self._repository = container.repository
        self._order_service = container.order_service
        self._payment_service = container.payment_service
        self._report_service = container.report_service

    def add_ped(self, n: str, its: list[LegacyItemPayload], t: str) -> int:
        return self._order_service.create_order(n, its, t)

    def get_ped(self, order_id: int) -> LegacyOrderPayload | None:
        return self._order_service.get_order(order_id)

    def upd_st(self, order_id: int, status: str) -> None:
        self._order_service.update_status(order_id, status)

    def calc_tot_cli(self, n: str) -> float:
        return self._report_service.calc_total_by_customer(n)

    def gerar_rel(self, tipo: str) -> None:
        self._report_service.generate(tipo)

    def proc_pag(self, order_id: int, method: str, value: float) -> bool:
        order = self._order_service.get_order_entity(order_id)
        if order is None:
            print("Metodo de pagamento invalido!")
            return False
        return self._payment_service.process_payment(
            order_id=order_id,
            method=method,
            value=value,
            order_total=order.total,
        )

    def validar_estoque(self, its: list[LegacyItemPayload]) -> bool:
        return self._order_service.validate_stock(its)

    def cancelar_pedido(self, order_id: int) -> None:
        self._order_service.cancel_order(order_id)

    def close(self) -> None:
        self._repository.close()


class PedEspecial:
    def __init__(self, db_path: str = "loja.db") -> None:
        container = build_special_app_container(db_path)
        self._repository = container.repository
        self._order_service = container.order_service

    def add_ped(self, n: str, its: list[LegacyItemPayload], t: str) -> int:
        return self._order_service.create_order(n, its, t)

    def get_ped(self, order_id: int) -> LegacyOrderPayload | None:
        return self._order_service.get_order(order_id)

    def upd_st(self, order_id: int, status: str) -> None:
        self._order_service.update_status(order_id, status)

    def close(self) -> None:
        self._repository.close()
