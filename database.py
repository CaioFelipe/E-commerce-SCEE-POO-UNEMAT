import sqlite3

class Database:
    def __init__(self, db_name="scee_loja.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row # Permite acessar colunas por nome
        return conn

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Produtos [cite: 428]
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sku TEXT UNIQUE NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                imagem_url TEXT,
                estoque INTEGER NOT NULL
            )
        ''')
        
        # Inserir dados mockados para visualização inicial (Seed)
        cursor.execute("SELECT count(*) FROM produtos")
        if cursor.fetchone()[0] == 0:
            produtos_iniciais = [
                ("Notebook Ultra Slim i7", "NB-001", "8GB RAM, 256GB SSD", 3500.00, "https://placehold.co/300x300/png?text=Notebook", 10),
                ("Smartphone Galaxy X", "SP-002", "Câmera 108MP, 128GB", 1999.90, "https://placehold.co/300x300/png?text=Smartphone", 20),
                ("Fone Bluetooth Pro", "AC-003", "Cancelamento de Ruído", 299.00, "https://placehold.co/300x300/png?text=Fone", 50),
                ("Monitor Gamer 24'", "MN-004", "144Hz, 1ms", 1200.00, "https://placehold.co/300x300/png?text=Monitor", 15)
            ]
            cursor.executemany("INSERT INTO produtos (nome, sku, descricao, preco, imagem_url, estoque) VALUES (?, ?, ?, ?, ?, ?)", produtos_iniciais)
            conn.commit()

        conn.close()

# Instância Singleton do Banco
db = Database()
