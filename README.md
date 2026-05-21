# Loja Verde - Sprint 2

Refatoracao guiada por SOLID, Clean Code e padroes GoF para o sistema legado de pedidos.

## Estrutura

```text
src/
  factories/
  interfaces/
  models/
  observers/
  repositories/
  services/
  strategies/
tests/
  golden_master/
  unit/
docs/
```

## Padroes aplicados

- Strategy para descontos, ajustes de pedido e metodos de pagamento
- Repository para isolamento do SQLite
- Observer para notificacoes
- Factory Method para criacao de pedidos

## Extensoes obrigatorias

- Pagamento em criptomoeda com taxa de 2%
- Notificacao por WhatsApp para todos os clientes
- Desconto por volume para 3+ unidades do mesmo item

## Comandos

```bash
make test
make cov
make lint
make type
make complexity
make all
```
