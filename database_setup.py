import sqlite3
import os
from config import Config
from argon2 import PasswordHasher

ph = PasswordHasher()

def create_tables():
    print(f"Recriando banco de dados completo em: {Config.DB_PATH}")
    
    # Remove banco antigo para garantir estrutura limpa
    if os.path.exists(Config.DB_PATH):
        try:
            os.remove(Config.DB_PATH)
            print("⚠️  Banco de dados antigo removido.")
        except PermissionError:
            print("❌ ERRO CRÍTICO: Feche o terminal do servidor (main.py) e tente novamente!")
            return

    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    # --- 1. USUÁRIOS E CLIENTES ---
    cursor.execute("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_completo TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('cliente', 'admin')),
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE clientes_info (
        usuario_id INTEGER PRIMARY KEY,
        cpf TEXT UNIQUE,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE enderecos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    );
    """)

    # --- 2. CATÁLOGO (CATEGORIAS E PRODUTOS) ---
    cursor.execute("""
    CREATE TABLE categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL CHECK(preco >= 0),
        estoque INTEGER NOT NULL DEFAULT 0 CHECK(estoque >= 0),
        categoria_id INTEGER,
        imagem_url TEXT,
        FOREIGN KEY(categoria_id) REFERENCES categorias(id)
    );
    """)

    # --- 3. VENDAS E PEDIDOS ---
    cursor.execute("""
    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Processando',
        total REAL NOT NULL,
        endereco_entrega TEXT NOT NULL,
        metodo_pagamento TEXT,
        codigo_rastreio TEXT,  -- COLUNA NOVA
        FOREIGN KEY(cliente_id) REFERENCES usuarios(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL CHECK(quantidade > 0),
        preco_unitario REAL NOT NULL,
        FOREIGN KEY(pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    );
    """)

    # --- 4. CARRINHO (PERSISTÊNCIA) ---
    cursor.execute("""
    CREATE TABLE carrinhos (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        usuario_id INTEGER NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
    );
    """)
    
    cursor.execute("""
    CREATE TABLE itens_carrinho (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        carrinho_id INTEGER NOT NULL, 
        produto_id INTEGER NOT NULL, 
        quantidade INTEGER NOT NULL,
        FOREIGN KEY(carrinho_id) REFERENCES carrinhos(id) ON DELETE CASCADE,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
    );
    """)

    # --- 5. DADOS INICIAIS (SEED) ---
    try:
        # Criar Admin
        senha_hash = ph.hash("admin123")
        cursor.execute("INSERT INTO usuarios (nome_completo, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
                      ("Ana Gerente", "ana@scee.com", senha_hash, "admin"))
        
        # Criar Categorias Iniciais
        categorias = [('Hardware',), ('Periféricos',), ('Monitores',), ('Computadores',)]
        cursor.executemany("INSERT INTO categorias (nome) VALUES (?)", categorias)
        
        print("✅ Tabelas criadas. Admin 'Ana' e Categorias inseridos.")
    except Exception as e:
        print(f"⚠️ Aviso no Seed inicial: {e}")

    conn.commit()
    conn.close()
    print("🚀 Banco de dados pronto para uso!")

if __name__ == "__main__":
    create_tables()