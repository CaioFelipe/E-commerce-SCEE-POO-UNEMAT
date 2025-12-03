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
    direction TD

    %% =======================================================
    %% 1. CAMADA DE APRESENTAÇÃO (FRONTEND)
    %% =======================================================
    namespace Frontend {
        class InterfaceWeb {
            +renderizar_pagina_html()
            +enviar_requisicao_api()
        }
    }

    %% =======================================================
    %% 2. CAMADA DE LÓGICA DE NEGÓCIOS (BACKEND)
    %% =======================================================
    namespace Backend {
        %% --- SERVIÇOS ---
        class AuthService {
            <<Serviço>>
            -_repo: UsuarioRepository
            +login(email, senha) dict
        }
        class CatalogoService {
            <<Serviço>>
            -_repo: ProdutoRepository
            +listar_produtos() List
            +buscar_produto(id) Produto
            +criar_produto(dados) Produto
        }
        class VendasService {
            <<Serviço>>
            -_pedido_repo: PedidoRepository
            -_endereco_repo: EnderecoRepository
            +realizar_checkout(uid, dados) int
        }

        %% --- PAGAMENTO ---
        class GatewayPagamento {
            <<Interface>>
            +processar_pagamento(valor, dados)* bool
        }
        class PagamentoPix {
            <<Serviço>>
            +processar_pagamento(valor, dados) bool
        }
        class PagamentoCartao {
            <<Serviço>>
            +processar_pagamento(valor, dados) bool
        }
        class FabricaPagamento {
            <<Factory>>
            +criar(tipo)$ Gateway
        }

        %% --- ENTIDADES E OBJETOS ---
        class Usuario {
            <<Abstract>>
            #_id: int
            #_nome: str
            #_email: str
            +verificar_senha(senha) bool
            +obter_permissao_acesso()* dict
        }
        class Cliente {
            <<Objeto>>
            -_cpf: str
            +validar_cpf() bool
        }
        class Administrador {
            <<Objeto>>
            +tem_acesso_total() bool
        }
        class Produto {
            <<Objeto>>
            -_sku: str
            -_preco: float
            -_estoque: int
            -_categoria_id: int
            +verificar_disponibilidade(qtd) bool
            +baixar_estoque(qtd)
        }
        class Categoria {
            <<Objeto>>
            -_nome: str
            -_descricao: str
        }
        class Pedido {
            <<Objeto>>
            -_total: float
            -_status: str
            -_itens: List~ItemPedido~
            +pode_ser_cancelado() bool
        }
        class ItemPedido {
            <<Objeto>>
            -_quantidade: int
            -_preco_unitario: float
            +subtotal() float
        }
        class Carrinho {
            <<Objeto>>
            -_itens: List~ItemCarrinho~
            +total() float
            +adicionar_item(item)
        }
        class ItemCarrinho {
            <<Objeto>>
            -_quantidade: int
            -_preco: float
            +subtotal() float
        }
        class Endereco {
            <<Objeto>>
            -_rua: str
            -_cep: str
        }
    }

    %% =======================================================
    %% 3. CAMADA DE DADOS (PERSISTÊNCIA)
    %% =======================================================
    namespace Persistencia {
        class BaseRepository {
            <<Interface>>
            +buscar_por_id(id)*
            +salvar(entidade)*
        }
        class UsuarioRepository {
            <<Dados>>
            +buscar_por_email(email) Usuario
        }
        class ProdutoRepository {
            <<Dados>>
            +listar_todos(filtros) List
        }
        class PedidoRepository {
            <<Dados>>
            +criar_pedido_atomico(uid, itens...) int
        }
        class EnderecoRepository {
            <<Dados>>
            +salvar_ou_atualizar(uid, dados)
        }
    }

    %% =======================================================
    %% RELACIONAMENTOS
    %% =======================================================

    %% Frontend -> Backend
    Frontend.InterfaceWeb ..> Backend.AuthService : Usa
    Frontend.InterfaceWeb ..> Backend.CatalogoService : Usa
    Frontend.InterfaceWeb ..> Backend.VendasService : Usa

    %% Backend Interno
    Backend.Usuario <|-- Backend.Cliente
    Backend.Usuario <|-- Backend.Administrador
    Backend.Pedido *-- Backend.ItemPedido
    Backend.Carrinho *-- Backend.ItemCarrinho
    Backend.Produto --> Backend.Categoria : Tem Categoria

    %% Pagamento
    Backend.GatewayPagamento <|.. Backend.PagamentoPix
    Backend.GatewayPagamento <|.. Backend.PagamentoCartao
    Backend.FabricaPagamento ..> Backend.GatewayPagamento : Cria
    Backend.VendasService ..> Backend.FabricaPagamento : Usa

    %% Backend -> Persistência (Injeção)
    Backend.AuthService --> Persistencia.UsuarioRepository : Usa
    Backend.CatalogoService --> Persistencia.ProdutoRepository : Usa
    Backend.VendasService --> Persistencia.PedidoRepository : Usa
    Backend.VendasService --> Persistencia.EnderecoRepository : Usa

    %% Retorno de Objetos
    Persistencia.UsuarioRepository ..> Backend.Usuario : Retorna
    Persistencia.ProdutoRepository ..> Backend.Produto : Retorna
    Persistencia.PedidoRepository ..> Backend.Pedido : Retorna

    %% Implementação de Repositórios
    Persistencia.BaseRepository <|.. Persistencia.UsuarioRepository
    Persistencia.BaseRepository <|.. Persistencia.ProdutoRepository
    Persistencia.BaseRepository <|.. Persistencia.PedidoRepository
