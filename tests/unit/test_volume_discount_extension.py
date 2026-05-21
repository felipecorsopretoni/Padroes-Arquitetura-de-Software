from legacy import Sis


def test_desconto_por_volume_aplica_quinze_por_cento(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sis = Sis()
    try:
        itens = [{"nome": "produto1", "p": 100, "q": 3, "tipo": "normal"}]
        pedido_id = sis.add_ped("Ana", itens, "normal")

        assert sis.get_ped(pedido_id)["tot"] == 255.0
    finally:
        sis.close()
