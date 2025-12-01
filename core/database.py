import sqlite3
from config import Config

def get_db_connection():
    """Cria uma conexão com o banco SQLite configurado."""
    conn = sqlite3.connect(Config.DB_PATH)
    # Permite acessar colunas como dicionários: linha['nome']
    conn.row_factory = sqlite3.Row 
    # Ativa Foreign Keys (Obrigatório para RNF07.2)
    conn.execute("PRAGMA foreign_keys = ON") 
    return conn