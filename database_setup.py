import sqlite3
import os
from config import Config
from argon2 import PasswordHasher

ph = PasswordHasher()

def create_tables():
    print(f"Recriando banco de dados em: {Config.DB_PATH}")
    
    if os.path.exists(Config.DB_PATH):
        try:
            os.remove(Config.DB_PATH)
            print("Banco antigo removido.")
        except PermissionError:
            print("ERRO: Feche o terminal do servidor (main.py) antes de rodar este script!")
            return

    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    # --- TABELAS ---
    
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

    # NOVA TABELA: ENDEREÇOS
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

    cursor.execute("""
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT UNIQUE NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL CHECK(preco >= 0),
        estoque INTEGER NOT NULL DEFAULT 0 CHECK(estoque >= 0),
        categoria_id INTEGER,
        imagem_url TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Processando',
        total REAL NOT NULL,
        endereco_entrega TEXT NOT NULL,
        metodo_pagamento TEXT,
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

    # Tabelas de Carrinho (Opcional se usar LocalStorage, mas mantemos estrutura)
    cursor.execute("CREATE TABLE carrinhos (id INTEGER PRIMARY KEY, usuario_id INTEGER);")
    cursor.execute("CREATE TABLE itens_carrinho (id INTEGER PRIMARY KEY, carrinho_id INTEGER, produto_id INTEGER, quantidade INTEGER);")

    # --- SEED INICIAL ---
    try:
        senha_hash = ph.hash("admin123")
        cursor.execute("INSERT INTO usuarios (nome_completo, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
                      ("Ana Gerente", "ana@scee.com", senha_hash, "admin"))
        print("Admin 'Ana' criado.")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

    conn.commit()
    conn.close()
    print("Banco de dados pronto! (Lembre-se de rodar o 'run_seed.py' para ter produtos)")

if __name__ == "__main__":
    create_tables()