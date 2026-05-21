from legacy import Sis


def test_notificacao_whatsapp_para_todos_os_tipos(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    sis = Sis()
    try:
        itens = [{"nome": "produto1", "p": 100, "q": 1, "tipo": "normal"}]
        sis.add_ped("Ana", itens, "normal")

        captured = capsys.readouterr()
        assert "WhatsApp enviado para Ana: Pedido recebido!" in captured.out
    finally:
        sis.close()
