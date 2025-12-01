from core.database import get_db_connection
from core.models.produto import Produto

class ProdutoRepository:
    def listar_todos(self):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM produtos").fetchall()
        conn.close()
        return [dict(row) for row in rows] # Retorna dicts para facilitar JSON

    def buscar_por_id(self, id):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row:
            return Produto(row['id'], row['sku'], row['nome'], row['preco'], row['estoque'])
        return None

    def salvar(self, produto):
        conn = get_db_connection()
        try:
            if produto.id: # Atualizar
                conn.execute("""
                    UPDATE produtos SET nome=?, sku=?, preco=?, estoque=?, descricao=?
                    WHERE id=?
                """, (produto.nome, produto.sku, produto.preco, produto.estoque, produto.descricao, produto.id))
            else: # Criar novo
                cursor = conn.execute("""
                    INSERT INTO produtos (nome, sku, preco, estoque, descricao)
                    VALUES (?, ?, ?, ?, ?)
                """, (produto.nome, produto.sku, produto.preco, produto.estoque, produto.descricao))
                produto.id = cursor.lastrowid
            conn.commit()
            return produto
        finally:
            conn.close()