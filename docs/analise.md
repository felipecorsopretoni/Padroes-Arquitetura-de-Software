# Analise Final

## (a) Identificacao das violacoes SOLID

### SRP
- `legacy.py` concentrava criacao de pedidos, persistencia, notificacao, pagamento e relatorios.
- Regras de fidelidade e transicoes de status estavam misturadas no mesmo fluxo.

### OCP
- Cadeias de `if/elif` controlavam descontos por item e meios de pagamento.
- Novos canais de notificacao exigiriam alterar a implementacao central.

### LSP
- `PedEspecial` sobrescrevia comportamento sem manter as invariantes da classe base.
- A hierarquia foi eliminada por composicao para evitar substituicao incorreta.

### ISP
- A fachada antiga expunha varias responsabilidades sem contratos especificos.
- O repositorio nao era separado das demais colaboracoes.

### DIP
- Os modulos de aplicacao criavam concretos diretamente.
- Regras de negocio dependiam de detalhes de notificacao e pagamento.

## (b) Solucoes Implementadas

- `Repository`: `SQLiteOrderRepository` isola o SQLite e implementa `OrderRepositoryInterface`.
- `Strategy`: descontos por item, descontos por cliente, ajustes de pedido e pagamentos sao plugaveis.
- `Observer`: notificacoes sao publicadas para observers especializados.
- `Factory Method`: `OrderFactoryRegistry` cria pedidos conforme o tipo de cliente.
- `DIP`: servicos recebem abstracoes no construtor e a composicao fica concentrada em `src/main.py`.
- `LSP`: `PedEspecial` deixa de herdar `Sis` e passa a usar composicao.

## (c) Diagrama UML de Classes

Ver `docs/diagrama.puml`.

## (d) Melhorias de Clean Code

- Extracao de entidades explicitas: `Customer`, `Order`, `OrderItem`.
- Reducao de metodos longos em servicos menores e coesos.
- Eliminacao de duplicacao nas regras de notificacao e pagamento.
- Centralizacao da composicao da aplicacao em um container simples.

## (e) Extensoes Implementadas

### Pagamento em criptomoeda
- Adiciona uma nova estrategia de pagamento.
- Entra no sistema sem alterar `PaymentService`.

### Notificacao via WhatsApp
- Adiciona um novo observer.
- Entra no fluxo sem alterar `NotificationService`.

### Desconto por volume
- Adiciona uma estrategia de ajuste de pedido.
- Entra no pipeline sem alterar `OrderService` nem `PricingService`.

## (f) Reflexao metacognitiva

### Principio ainda em evolucao
- LSP continua sendo o principio que mais exige disciplina ao decidir entre heranca e composicao.

### Uso de IA
- A IA foi usada para acelerar refatoracoes mecanicas, revisar consistencia e organizar artefatos.
- As decisoes finais foram mantidas alinhadas ao comportamento legado e ao enunciado.
