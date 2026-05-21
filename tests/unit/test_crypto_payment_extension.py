from legacy import Sis


def test_pagamento_em_criptomoeda_aprova_com_taxa(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sis = Sis()
    try:
        itens = [{"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"}]
        pedido_id = sis.add_ped("Ana", itens, "normal")

        assert sis.proc_pag(pedido_id, "criptomoeda", 102) is True
        assert sis.get_ped(pedido_id)["st"] == "aprovado"
    finally:
        sis.close()
