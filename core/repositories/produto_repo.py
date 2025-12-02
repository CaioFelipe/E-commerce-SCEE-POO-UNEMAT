from core.database import get_db_connection
from core.models.produto import Produto

class ProdutoRepository:
    def listar_todos(self, filtros=None):
        conn = get_db_connection()
        # Faz JOIN com categorias para mostrar o nome da categoria na lista
        query = """
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE 1=1
        """
        params = []

        if filtros:
            # Filtro por Categoria
            if 'categoria_id' in filtros and filtros['categoria_id']:
                query += " AND p.categoria_id = ?"
                params.append(int(filtros['categoria_id']))

            # Filtro por Texto (Nome, Descrição ou SKU)
            if 'termo' in filtros and filtros['termo']:
                query += " AND (p.nome LIKE ? OR p.descricao LIKE ? OR p.sku LIKE ?)"
                termo = f"%{filtros['termo']}%"
                params.extend([termo, termo, termo])

            # Filtros de Preço
            if 'min_price' in filtros and filtros['min_price']:
                query += " AND p.preco >= ?"
                params.append(float(filtros['min_price']))
            if 'max_price' in filtros and filtros['max_price']:
                query += " AND p.preco <= ?"
                params.append(float(filtros['max_price']))

        query += " ORDER BY p.nome ASC"

        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def listar_categorias(self):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM categorias ORDER BY nome").fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def buscar_por_id(self, id):
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
        conn.close()
        if row:
            # Retorna objeto Produto padrão (sem campos extras do join para edição)
            prod = Produto(row['id'], row['sku'], row['nome'], row['preco'], row['estoque'])
            prod.descricao = row['descricao']
            prod.imagem_url = row['imagem_url']
            prod.categoria_id = row['categoria_id']
            return prod
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