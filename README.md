# **SCEE \- Sistema de Comércio Eletrônico de Eletrônicos**

O **SCEE** é uma plataforma híbrida de e-commerce desenvolvida em Python, focada em eficiência operacional e vendas. O sistema utiliza uma arquitetura moderna separando o núcleo (Backend) das interfaces de consumo (Web e Desktop).

## **🚀 Arquitetura**

O sistema segue o padrão de **3 Camadas** com uma abordagem de API RESTful:

1. **Backend (Core & API):**  
   * Linguagem: Python 3.10+  
   * Framework Web: Flask (Expondo JSON via Blueprints)  
   * Banco de Dados: SQLite (Com Transações Atômicas)  
   * Segurança: JWT (JSON Web Token) e Argon2 (Hash de Senha)  
   * Destaques: Polimorfismo em Usuários e Pagamentos, Transações ACID.  
2. **Frontend Web (Cliente Final \- Carlos):**  
   * Tecnologia: HTML5, CSS3 (Dark Mode), JavaScript (Vanilla ES6+).  
   * Responsabilidade: Catálogo, Carrinho de Compras e Checkout.  
3. **Frontend Desktop (Gestão \- Ana):**  
   * Tecnologia: Python Tkinter.  
   * Responsabilidade: CRUD de Produtos, Upload de Imagens, Gestão de Pedidos.

## **🛠️ Pré-requisitos**

* Python 3.10 ou superior instalado.  
* Navegador Web Moderno (Chrome, Firefox, Edge).

## **📦 Instalação**

1. **Clone o repositório** (ou extraia os arquivos):  
   git clone \[https://github.com/seu-usuario/scee.git\](https://github.com/seu-usuario/scee.git)  
   cd scee

2. **Crie um Ambiente Virtual (Recomendado):**  
   * *Windows:* python \-m venv venv  
   * *Linux/Mac:* python3 \-m venv venv  
3. **Ative o Ambiente Virtual:**  
   * *Windows:* venv\\Scripts\\activate  
   * *Linux/Mac:* source venv/bin/activate  
4. **Instale as dependências:**  
   pip install \-r requirements.txt

5. **Configure o Ambiente:**  
   * Renomeie o arquivo config.example.py para config.py.  
   * (Opcional) Edite a SECRET\_KEY dentro dele.  
6. Inicialize o Banco de Dados:  
   Execute o script que cria as tabelas e o usuário admin inicial.  
   python database\_setup.py

   *Isso criará o arquivo scee\_loja.db na raiz.*

## **▶️ Como Rodar**

### **1\. Iniciar o Servidor (Backend)**

Mantenha este terminal aberto. O servidor deve rodar para que os clientes funcionem.

python main.py

*O servidor iniciará em http://127.0.0.1:5000.*

### **2\. Acessar a Loja Web (Cliente)**

* Navegue até a pasta web\_client.  
* Abra o arquivo index.html no seu navegador.  
* *Nota:* Para login, você pode criar um cliente via API ou usar o admin para testes iniciais.

### **3\. Acessar a Gestão (Desktop)**

Abra um **novo terminal**, ative o ambiente virtual e execute:

python \-m desktop\_client.main\_app

* **Login Padrão (Criado pelo database\_setup.py):**  
  * E-mail: ana@scee.com  
  * Senha: admin123 (Nota: Em produção, o hash seria verificado, no setup inicial usamos placeholder ou hash real se implementado).

## **📚 Funcionalidades Chave**

* **Polimorfismo:** Usuários (Cliente/Admin) e Pagamentos (Pix/Cartão) comportam-se de forma distinta usando a mesma interface.  
* **Transação Atômica:** O checkout garante que o pedido só é criado se o estoque for baixado com sucesso.  
* **JWT:** Autenticação stateless segura entre Desktop e Web.