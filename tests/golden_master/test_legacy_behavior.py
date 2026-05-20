import pytest
from legacy import Sis

@pytest.fixture
def sis(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = Sis()
    yield s
    s.close()

def test_pedido_normal_calcula_total_corretamente(sis):
    itens = [
        {'nome': 'produto1', 'p': 100, 'q': 2, 'tipo': 'normal'},
        {'nome': 'produto2', 'p': 50,  'q': 1, 'tipo': 'desc10'},
    ]
    id_ped = sis.add_ped('Joao Silva', itens, 'normal')
    pedido = sis.get_ped(id_ped)
    assert pedido['tot'] == pytest.approx(245.0)
    assert pedido['st'] == 'pendente'
    assert pedido['tp'] == 'normal'

def test_pedido_vip_aplica_desconto_5_porcento(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Maria', itens, 'vip')
    assert sis.get_ped(id_ped)['tot'] == pytest.approx(95.0)

def test_pedido_corporativo_aplica_desconto_10_porcento(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Empresa XYZ', itens, 'corporativo')
    assert sis.get_ped(id_ped)['tot'] == pytest.approx(90.0)

def test_cartao_aprova_pedido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    resultado = sis.proc_pag(id_ped, 'cartao', 100)
    assert resultado is True
    assert sis.get_ped(id_ped)['st'] == 'aprovado'

def test_pix_aprova_pedido_automaticamente(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.proc_pag(id_ped, 'pix', 100)
    assert sis.get_ped(id_ped)['st'] == 'aprovado'

def test_boleto_nao_aprova_automaticamente(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.proc_pag(id_ped, 'boleto', 100)
    assert sis.get_ped(id_ped)['st'] == 'pendente'

def test_atualizacao_de_status(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.upd_st(id_ped, 'aprovado')
    assert sis.get_ped(id_ped)['st'] == 'aprovado'

def test_cancelamento_de_pedido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.cancelar_pedido(id_ped)
    assert sis.get_ped(id_ped)['st'] == 'cancelado'

def test_relatorio_vendas_nao_lanca_excecao(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Joao', itens, 'normal')
    sis.gerar_rel('vendas')

def test_pagamento_insuficiente_retorna_false(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    assert sis.proc_pag(id_ped, 'cartao', 50) is False


    # Cobre desc20 e frete_gratis (linhas 23-26)
def test_item_desc20(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc20'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    assert sis.get_ped(id_ped)['tot'] == pytest.approx(80.0)

def test_item_frete_gratis(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'frete_gratis'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    assert sis.get_ped(id_ped)['tot'] == pytest.approx(100.0)

# Cobre get_ped com id inexistente (linha 56)
def test_get_ped_inexistente(sis):
    assert sis.get_ped(9999) is None

# Cobre upd_st enviado e entregue com pontos (linhas 66-79)
def test_status_enviado(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.upd_st(id_ped, 'enviado')
    assert sis.get_ped(id_ped)['st'] == 'enviado'

def test_status_entregue_normal(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    sis.upd_st(id_ped, 'entregue')
    assert sis.get_ped(id_ped)['st'] == 'entregue'

def test_status_entregue_vip(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Maria', itens, 'vip')
    sis.upd_st(id_ped, 'entregue')
    assert sis.get_ped(id_ped)['st'] == 'entregue'

def test_status_entregue_corporativo(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Empresa', itens, 'corporativo')
    sis.upd_st(id_ped, 'entregue')
    assert sis.get_ped(id_ped)['st'] == 'entregue'

# Cobre calc_tot_cli (linhas 82-87)
def test_calc_tot_cli(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]

# Cobre linhas 66-79 (upd_st aprovado com vip)
def test_status_aprovado_vip(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Maria', itens, 'vip')
    sis.upd_st(id_ped, 'aprovado')
    assert sis.get_ped(id_ped)['st'] == 'aprovado'

# Cobre linhas 82-87 (calc_tot_cli)
def test_calc_tot_cli_zero(sis):
    assert sis.calc_tot_cli('Ninguem') == 0

# Cobre linhas 101-112 (gerar_rel clientes)
def test_relatorio_clientes(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    sis.add_ped('Joao', itens, 'vip')
    sis.gerar_rel('clientes')

# Cobre linha 117 (proc_pag pedido inexistente)
def test_proc_pag_pedido_inexistente(sis):
    assert sis.proc_pag(9999, 'cartao', 100) is False

# Cobre linhas 136-137 (pagamento invalido)
def test_pagamento_metodo_desconhecido(sis):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = sis.add_ped('Joao', itens, 'normal')
    assert sis.proc_pag(id_ped, 'cheque', 100) is False

# Cobre linhas 140-148 (validar_estoque)
def test_validar_estoque_pass(sis):
    itens = [{'nome': 'produto2', 'p': 50, 'q': 1, 'tipo': 'normal'}]
    assert sis.validar_estoque(itens) is True

def test_validar_estoque_sem_estoque(sis):
    itens = [{'nome': 'produto1', 'p': 100, 'q': 500, 'tipo': 'normal'}]
    assert sis.validar_estoque(itens) is False

def test_validar_estoque_nome_invalido(sis):
    itens = [{'nome': 'inexistente', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    assert sis.validar_estoque(itens) is False

# Cobre linhas 161-184 (PedEspecial) usando fixture isolada
@pytest.fixture
def ped_especial(tmp_path, monkeypatch):
    from legacy import PedEspecial
    monkeypatch.chdir(tmp_path)
    pe = PedEspecial()
    yield pe
    pe.close()

def test_ped_especial_normal(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Joao', itens, 'normal')
    assert ped_especial.get_ped(id_ped)['tot'] == pytest.approx(115.0)

def test_ped_especial_desc10(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc10'}]
    id_ped = ped_especial.add_ped('Joao', itens, 'normal')
    assert ped_especial.get_ped(id_ped)['tot'] == pytest.approx(103.5)

def test_ped_especial_desc20(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'desc20'}]
    id_ped = ped_especial.add_ped('Joao', itens, 'normal')
    assert ped_especial.get_ped(id_ped)['tot'] == pytest.approx(92.0)

def test_ped_especial_upd_st_aprovado(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Joao', itens, 'normal')
    ped_especial.upd_st(id_ped, 'aprovado')
    assert ped_especial.get_ped(id_ped)['st'] == 'aprovado'

def test_ped_especial_upd_st_entregue(ped_especial):
    itens = [{'nome': 'p1', 'p': 100, 'q': 1, 'tipo': 'normal'}]
    id_ped = ped_especial.add_ped('Joao', itens, 'normal')
    ped_especial.upd_st(id_ped, 'entregue')
    assert ped_especial.get_ped(id_ped)['st'] == 'entregue'