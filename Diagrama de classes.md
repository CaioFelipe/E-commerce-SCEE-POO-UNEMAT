# Sistema de E-commerce Modular (Python)

Este repositório contém a implementação de um núcleo de sistema de E-commerce desenvolvido em Python, focado em **Arquitetura em Camadas**, **Princípios SOLID** e **Padrões de Projeto** (Design Patterns).

O objetivo é demonstrar uma separação clara de responsabilidades entre a interface do usuário, as regras de negócio e a persistência de dados.

## 🏛️ Visão Geral da Arquitetura

O sistema foi modelado seguindo uma arquitetura de 3 camadas estritas:

1.  **Camada de Apresentação (Frontend):** Responsável apenas pela interação com o usuário (HTML/CSS/JS). Ela não contém regras de negócio, apenas consome a API do Backend.
2.  **Camada de Lógica de Negócios (Backend):** O coração do sistema. Contém os **Serviços** (Services), **Objetos de Domínio** (Entities/Value Objects) e interfaces. Aqui residem as regras de validação, cálculo de totais e orquestração de fluxos.
3.  **Camada de Dados (Persistência):** Responsável pelo acesso ao banco de dados (SQLite). Utiliza o padrão **Repository** para abstrair consultas SQL, permitindo que o Backend permaneça agnóstico em relação à tecnologia de banco de dados.

## 📊 Diagrama de Classes (UML)

O diagrama abaixo ilustra a estrutura das classes, a organização em `namespaces` (camadas) e os relacionamentos de herança, composição e dependência.

> **Nota:** Este diagrama é renderizado nativamente pelo GitHub. Se estiver visualizando em outro editor, certifique-se de ter suporte a [Mermaid JS](https://mermaid.js.org/).

```mermaid
classDiagram
    %% Estereótipos
    class Usuario {
        <<Abstract>>
        #_id: int
        #_nome: string
        #_email: string
        #_senha_hash: string
        #_tipo: string
        +__init__(id, nome, email, senha_hash, tipo)
        +gerar_hash(senha_plana)$
        +verificar_senha(senha_plana) bool
        +obter_permissao_acesso()* dict
    }

    class Cliente {
        <<Entity>>
        -_cpf: string
        +__init__(id, nome, email, senha_hash, cpf)
        +obter_permissao_acesso() dict
        +validar_cpf() bool
    }

    class Administrador {
        <<Entity>>
        +__init__(id, nome, email, senha_hash)
        +obter_permissao_acesso() dict
        +tem_acesso_total() bool
    }

    class Produto {
        <<Entity>>
        -_id: int
        -_sku: string
        -_nome: string
        -_preco: float
        -_estoque: int
        -_descricao: string
        -_categoria_id: int
        -_imagem_url: string
        +__init__(id, sku, nome, preco, estoque)
        +verificar_disponibilidade(quantidade_solicitada) bool
        +baixar_estoque(quantidade)
    }

    class Categoria {
        <<Entity>>
        -_id: int
        -_nome: string
        -_descricao: string
        +__init__(id, nome, descricao)
    }

    class Pedido {
        <<Aggregate Root>>
        -_id: int
        -_cliente_id: int
        -_data_pedido: datetime
        -_total: float
        -_endereco_entrega: string
        -_status: string
        -_itens: List~ItemPedido~
        +STATUS_PROCESSANDO: str$
        +STATUS_ENVIADO: str$
        +STATUS_CANCELADO: str$
        +__init__(id, cliente_id, data_pedido, total, endereco_entrega, status, itens)
        +pode_ser_cancelado() bool
    }

    class ItemPedido {
        <<Entity>>
        -_id: int
        -_pedido_id: int
        -_produto_id: int
        -_quantidade: int
        -_preco_unitario: float
        -_nome_produto: string
        +__init__(id, pedido_id, produto_id, quantidade, preco_unitario, nome_produto)
        +subtotal() float
    }

    class Carrinho {
        <<Entity>>
        -_usuario_id: int
        -_itens: List~ItemCarrinho~
        +__init__(usuario_id, itens)
        +total() float
        +adicionar_item(item: ItemCarrinho)
        +remover_item(produto_id)
        +limpar()
        +to_dict() dict
    }

    class ItemCarrinho {
        <<Value Object>>
        -_produto_id: int
        -_quantidade: int
        -_preco_unitario: float
        -_nome_produto: string
        +__init__(produto_id, quantidade, preco_unitario, nome_produto)
        +subtotal() float
        +to_dict() dict
    }

    class Endereco {
        <<Value Object>>
        -_id: int
        -_usuario_id: int
        -_rua: string
        -_numero: string
        -_bairro: string
        -_cidade: string
        -_estado: string
        -_cep: string
        +__init__(id, usuario_id, rua, numero, bairro, cidade, estado, cep)
        +__str__() string
    }

    %% Interfaces e Serviços
    class GatewayPagamento {
        <<Interface>>
        +processar_pagamento(valor, dados_pagamento)* bool, str
    }

    class PagamentoPix {
        <<Service>>
        +processar_pagamento(valor, dados_pagamento) bool, str
    }

    class PagamentoCartao {
        <<Service>>
        +processar_pagamento(valor, dados_pagamento) bool, str
    }

    class FabricaPagamento {
        <<Factory>>
        +criar(tipo)$ GatewayPagamento
    }

    class AuthService {
        <<Service>>
        -_repo: UsuarioRepository
        +login(email, senha_plana) dict
    }

    class CatalogoService {
        <<Service>>
        -_repo: ProdutoRepository
        +listar_produtos() List~dict~
        +buscar_produto(produto_id) Produto
        +criar_produto(dados_produto) Produto
    }

    class VendasService {
        <<Service>>
        -_pedido_repo: PedidoRepository
        -_endereco_repo: EnderecoRepository
        +realizar_checkout(usuario_id, dados_checkout) int
    }

    %% Repositórios
    class BaseRepository {
        <<Interface>>
        +buscar_por_id(id)*
        +listar_todos()*
        +salvar(entidade)*
        +deletar(id)*
    }

    class UsuarioRepository {
        <<Repository>>
        -_instanciar_correto(row) Usuario
        +buscar_por_email(email) Usuario
        +buscar_por_id(id) Usuario
        +criar(usuario) Usuario
        +atualizar(usuario) bool
        +listar_clientes() List~dict~
    }

    class ProdutoRepository {
        <<Repository>>
        +listar_todos(filtros) List~dict~
        +buscar_por_id(id) Produto
        +salvar(produto) Produto
        +listar_categorias() List~dict~
    }

    class PedidoRepository {
        <<Repository>>
        +criar_pedido_atomico(usuario_id, itens_carrinho, total, endereco, valor_frete) int
        +listar_todos() List~dict~
        +buscar_por_id_com_itens(pedido_id) dict
        +buscar_historico_cliente(cliente_id) List~dict~
        +atualizar_status(pedido_id, novo_status) bool
    }

    class EnderecoRepository {
        <<Repository>>
        +salvar_ou_atualizar(usuario_id, rua, numero, bairro)
        +buscar_por_usuario(usuario_id) dict
    }

    %% Relacionamentos
    Usuario <|-- Cliente : Herança
    Usuario <|-- Administrador : Herança
    
    GatewayPagamento <|.. PagamentoPix : Implementa
    GatewayPagamento <|.. PagamentoCartao : Implementa
    FabricaPagamento ..> GatewayPagamento : Cria

    Pedido *-- ItemPedido : Composição
    Carrinho *-- ItemCarrinho : Composição
    
    AuthService --> UsuarioRepository : Usa
    CatalogoService --> ProdutoRepository : Usa
    VendasService --> PedidoRepository : Usa
    VendasService --> EnderecoRepository : Usa
    VendasService ..> FabricaPagamento : Usa

    ProdutoRepository ..> Produto : Persiste
    PedidoRepository ..> Pedido : Persiste
    UsuarioRepository ..> Usuario : Persiste
    
    Produto --> Categoria : Pertence
