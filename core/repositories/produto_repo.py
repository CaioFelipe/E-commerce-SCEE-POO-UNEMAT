from core.database import get_db_connection
from core.models.produto import Produto

class ProdutoRepository:
    def listar_todos(self, filtros=None):
        conn = get_db_connection()
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []

        if filtros:
            # Filtro por Categoria (NOVO)
            if 'categoria_id' in filtros and filtros['categoria_id']:
                query += " AND categoria_id = ?"
                params.append(int(filtros['categoria_id']))

            if 'termo' in filtros and filtros['termo']:
                query += " AND (nome LIKE ? OR descricao LIKE ?)"
                termo = f"%{filtros['termo']}%"
                params.extend([termo, termo])

            if 'min_price' in filtros and filtros['min_price']:
                query += " AND preco >= ?"
                params.append(float(filtros['min_price']))

            if 'max_price' in filtros and filtros['max_price']:
                query += " AND preco <= ?"
                params.append(float(filtros['max_price']))

        query += " ORDER BY nome ASC"

        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def listar_categorias(self):
        """Retorna todas as categorias para preencher o select no frontend."""
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ... (buscar_por_id e salvar mantêm-se iguais, se precisares, copia do anterior) ...
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
            cursor = conn.cursor()
            if produto.id: 
                cursor.execute("""
                    UPDATE produtos SET nome=?, sku=?, preco=?, estoque=?, descricao=?, imagem_url=?, categoria_id=?
                    WHERE id=?
                """, (produto.nome, produto.sku, produto.preco, produto.estoque, produto.descricao, produto.imagem_url, getattr(produto, 'categoria_id', None), produto.id))
            else: 
                cursor.execute("""
                    INSERT INTO produtos (nome, sku, preco, estoque, descricao, imagem_url, categoria_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (produto.nome, produto.sku, produto.preco, produto.estoque, produto.descricao, produto.imagem_url, getattr(produto, 'categoria_id', None)))
                produto.id = cursor.lastrowid
            conn.commit()
            return produto
        finally:
            conn.close()