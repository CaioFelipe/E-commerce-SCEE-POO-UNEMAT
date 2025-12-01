import sqlite3
import os

DB_PATH = "scee_loja.db"
SQL_FILE = "populate_db.sql"

def run_seed():
    if not os.path.exists(DB_PATH):
        print(f"Erro: O banco de dados '{DB_PATH}' não foi encontrado.")
        return

    if not os.path.exists(SQL_FILE):
        print(f"Erro: O arquivo SQL '{SQL_FILE}' não foi encontrado.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        cursor.executescript(sql_script)
        conn.commit()
        print("✅ Sucesso! 8 produtos foram inseridos no banco de dados.")
        
        # Verifica
        cursor.execute("SELECT nome, preco FROM produtos")
        items = cursor.fetchall()
        for item in items:
            print(f" - {item[0]}: R$ {item[1]:.2f}")

    except sqlite3.Error as e:
        print(f"❌ Erro ao executar SQL: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_seed()