# **SCEE \- Sistema de Comércio Eletrônico de Eletrônicos**

O **SCEE** é uma plataforma completa de e-commerce desenvolvida em Python, focada em eficiência operacional e vendas. O sistema utiliza uma arquitetura híbrida de 3 camadas, separando o núcleo (Backend) das interfaces de consumo (Web para Clientes e Desktop para Gestão).

## **🚀 Destaques Técnicos**

O projeto foi construído seguindo rigorosamente os princípios de Engenharia de Software e POO:

* **Arquitetura Híbrida:** Backend Flask servindo API REST para um Frontend Web (JS Vanilla) e um Cliente Desktop (Tkinter).  
* **Polimorfismo:** Implementado na autenticação (Cliente vs Admin) e no Pagamento (Pix vs Cartão via Strategy Pattern).  
* **Transações ACID:** O checkout garante integridade atômica entre criação do pedido, baixa de estoque e registro financeiro.  
* **Segurança:** Hash de senhas com Argon2 e autenticação stateless via JWT.  
* **Persistência:** SQLite com chaves estrangeiras e integridade referencial ativadas.

## **🛠️ Tecnologias Utilizadas**

* **Backend:** Python 3.10+, Flask, SQLite3.  
* **Frontend Web:** HTML5, CSS3 (Dark Mode), JavaScript (ES6+), Fetch API.  
* **Desktop Client:** Python Tkinter (MVC Pattern).  
* **Bibliotecas:** flask-cors, argon2-cffi, PyJWT, requests.

## **📦 Instalação e Configuração**

### **1\. Preparar o Ambiente**

Clone o repositório e crie um ambiente virtual:

\# Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# Linux/Mac  
python3 \-m venv venv  
source venv/bin/activate

### **2\. Instalar Dependências**

pip install \-r requirements.txt

### **3\. Configurar Banco de Dados**

Execute os scripts para criar as tabelas e popular com dados de teste:

\# Cria as tabelas e o usuário Admin  
python database\_setup.py

\# Insere produtos e categorias de exemplo  
python run\_seed.py

## **▶️ Como Executar**

O sistema precisa que o **Servidor (Backend)** esteja rodando para que as interfaces funcionem.

### **Passo 1: Iniciar o Servidor (Backend)**

Abra um terminal e execute:

python main.py

*O servidor ficará online em http://127.0.0.1:5000.*

### **Passo 2: Acessar a Loja (Cliente)**

* Vá até a pasta web\_client.  
* Abra o arquivo index.html no seu navegador.  
* **Funcionalidades:** Cadastro, Login, Busca, Filtros, Carrinho, Checkout, Histórico de Pedidos.

### **Passo 3: Acessar a Gestão (Desktop)**

Abra um **novo terminal** (com o venv ativado) e execute:

python \-m desktop\_client.main\_app

* **Login de Administrador:**  
  * **E-mail:** ana@scee.com  
  * **Senha:** admin123  
* **Funcionalidades:** Dashboard de Pedidos, Detalhes com Itens, Alteração de Status (Rastreio), Cadastro/Edição de Produtos, Upload de Imagens, Listagem de Clientes.

## **📂 Estrutura do Projeto**

* /api: Rotas (Endpoints) separadas por contexto (Web vs Gestão).  
* /core: O coração do sistema. Contém Models (Regras de Negócio) e Repositories (SQL).  
* /services: Camada de orquestração (Regras de Aplicação).  
* /web\_client: Interface do cliente (SPA).  
* /desktop\_client: Interface da gestão (Tkinter).

## **📄 Licença**

Este projeto foi desenvolvido para fins educacionais da disciplina de POO.