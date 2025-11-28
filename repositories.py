from database import db
from models import Produto

class ProdutoRepositorio:
    def buscar_todos(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        rows = cursor.fetchall()
        conn.close()
        return [Produto(**dict(row)) for row in rows]

    def buscar_por_id(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Produto(**dict(row))
        return None
