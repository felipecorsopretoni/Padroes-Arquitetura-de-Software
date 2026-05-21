# 🛒 Loja Verde — Refatoração Guiada por SOLID

> EFC 1 — Padrões e Arquitetura de Software | PUC-Campinas | Prof. Dr. Douglas H. S. Abreu | 2026

---

## 📋 Sobre o Projeto

Este repositório contém a refatoração completa de um sistema legado de pedidos de e-commerce, aplicando os princípios **SOLID**, boas práticas de **Clean Code** e ao menos quatro padrões **GoF**. A refatoração é guiada por uma suíte de **Golden Master Tests** que garante ausência de regressão funcional ao longo de todo o processo.

---

## 🏗️ Estrutura do Projeto

```
projeto/
├── legacy.py
├── src/
│   ├── main.py
│   ├── factories/
│   ├── interfaces/
│   ├── models/
│   │   ├── order.py
│   │   ├── customer.py
│   │   └── order_item.py
│   ├── observers/
│   │   └── extensions/
│   ├── repositories/
│   ├── services/
│   └── strategies/
│       └── extensions/
├── tests/
│   ├── golden_master/
│   │   └── test_legacy_behavior.py
│   └── unit/
├── docs/
│   ├── analise.md
│   └── diagrama.puml
├── Makefile
├── pyproject.toml
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- pip

### Instalação

```bash
pip install pytest pytest-cov coverage ruff mypy radon
```

### Comandos disponíveis

```bash
make test        # Roda os testes
make cov         # Testes com relatório de cobertura
make lint        # Verificação de estilo (ruff)
make type        # Verificação de tipos (mypy --strict)
make complexity  # Complexidade ciclomática (radon)
make all         # Executa tudo acima
```

---

## 📊 Métricas

| Métrica | Resultado | Mínimo exigido |
|---|---|---|
| Cobertura de testes | **94%** | 80% |
| Testes passando | **31/31** | — |
| Lint (ruff) | — | score ≥ 8.5 |
| Complexidade ciclomática | — | nota B (CC ≤ 10) |
| Type hints (mypy) | — | sem erros |

---

## 🗓️ Sprints

### ✅ Sprint 0 — Golden Master Tests (entregue 14/05/2026)
- Suíte de 31 testes cobrindo todos os fluxos obrigatórios
- Cobertura de 94% medida por `coverage.py`
- Documento de análise textual com 2 violações por princípio SOLID
- Tag `sprint-0` criada

### ✅ Sprint 1 — SRP, ISP e separação em camadas (entregue 20/05/2026)
- Organização em camadas: `models`, `repositories`, `services`, `interfaces`
- Padrão Repository isolando acesso ao SQLite
- Interfaces abstratas (ABC) por camada de colaboração externa
- Tag `sprint-1` criada

### ✅ Sprint 2 — OCP, DIP, LSP e padrões GoF (entregue 26/05/2026)
- Strategy para descontos, ajustes de pedido e métodos de pagamento
- Observer para notificações desacopladas
- Factory Method para criação de pedidos por tipo de cliente
- Injeção de dependência explícita em todos os serviços
- Três extensões obrigatórias implementadas
- Tag `sprint-2` criada

---

## 🔧 Padrões GoF Aplicados

| Padrão | Aplicação |
|---|---|
| **Strategy** | Algoritmos de desconto por item, por cliente, ajuste de pedido e métodos de pagamento intercambiáveis |
| **Repository** | Isolamento do acesso ao SQLite via `SQLiteOrderRepository` |
| **Observer** | Notificações desacopladas da regra de negócio via `NotificationPublisher` |
| **Factory Method** | Criação de pedidos diferenciados por tipo de cliente via `OrderFactoryRegistry` |

---

## 🧩 Extensões Obrigatórias

Todas implementadas **sem modificar nenhuma classe existente**, provando OCP empiricamente:

- ✅ **Pagamento em criptomoeda** — taxa de 2% sobre o valor do pedido (`CryptoPaymentStrategy`)
- ✅ **Canal WhatsApp** — notificações para todos os tipos de cliente (`WhatsAppObserver`)
- ✅ **Desconto por volume** — 3+ unidades do mesmo item recebem 15% adicional (`VolumeDiscountStrategy`)

---

## 📐 Violações SOLID Identificadas (Sprint 0)

| Princípio | Violação | Localização |
|---|---|---|
| SRP | Classe `Sis` acumula DB, pagamento, notificação e relatório | `legacy.py` linhas 6–160 |
| SRP | Método `gerar_rel` faz query, print e gravação em disco | `legacy.py` linhas 90–114 |
| OCP | Cadeia `if/elif` para tipos de desconto | `legacy.py` linhas 19–26 |
| OCP | Cadeia `if/elif` para métodos de pagamento | `legacy.py` linhas 123–138 |
| LSP | `PedEspecial.upd_st` ignora notificações e pontos do pai | `legacy.py` linhas 183–190 |
| LSP | `PedEspecial.add_ped` quebra invariante de notificação por tipo | `legacy.py` linhas 164–181 |
| ISP | `Sis` expõe 9 métodos públicos para todos os clientes | `legacy.py` linhas 6–160 |
| ISP | Sem separação entre operações de leitura e escrita | `legacy.py` — ausência de interfaces |
| DIP | `sqlite3.connect` instanciado diretamente no construtor | `legacy.py` linha 8 |
| DIP | Notificações embutidas como `print()` dentro das regras de negócio | `legacy.py` linhas 39–48 |

---

## 📚 Referências

- Martin, R. C. *Clean Code*. Prentice Hall, 2008.
- Feathers, M. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
- Gamma, E. et al. *Design Patterns*. Addison-Wesley, 1994.
- Fowler, M. *Refactoring*. 2ª ed. Addison-Wesley, 2018.
