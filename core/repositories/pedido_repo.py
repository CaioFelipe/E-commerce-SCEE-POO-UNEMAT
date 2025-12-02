import sqlite3
from core.database import get_db_connection

class PedidoRepository:
    def criar_pedido_atomico(self, usuario_id, itens_carrinho, total, endereco):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.execute("BEGIN TRANSACTION;")
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, total, endereco_entrega, status, metodo_pagamento)
                VALUES (?, ?, ?, 'Processando', 'Desconhecido')
            """, (usuario_id, total, endereco))
            pedido_id = cursor.lastrowid

            for item in itens_carrinho:
                prod_id = item['produto_id']
                qtd = item['qtd']
                preco = item['preco_unitario']

                cursor.execute("SELECT estoque FROM produtos WHERE id = ?", (prod_id,))
                row = cursor.fetchone()
                if not row or row['estoque'] < qtd:
                    raise ValueError(f"Produto ID {prod_id} sem estoque suficiente.")

                cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (qtd, prod_id))
                cursor.execute("""
                    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                """, (pedido_id, prod_id, qtd, preco))

            conn.commit()
            return pedido_id
        except Exception as e:
            conn.rollback()
            print(f"Erro no Repo Pedido (Criar): {e}") # Debug no terminal
            raise e
        finally:
            conn.close()

    def buscar_historico_cliente(self, cliente_id):
        conn = get_db_connection()
        try:
            # 1. Busca os pedidos
            query_pedidos = """
                SELECT id, total, status, data_pedido, endereco_entrega 
                FROM pedidos 
                WHERE cliente_id = ? 
                ORDER BY id DESC
            """
            pedidos_rows = conn.execute(query_pedidos, (cliente_id,)).fetchall()
            pedidos = [dict(p) for p in pedidos_rows]

            # 2. Para cada pedido, busca os itens
            for p in pedidos:
                query_itens = """
                    SELECT ip.quantidade, ip.preco_unitario, pr.nome, pr.imagem_url
                    FROM itens_pedido ip
                    JOIN produtos pr ON ip.produto_id = pr.id
                    WHERE ip.pedido_id = ?
                """
                itens_rows = conn.execute(query_itens, (p['id'],)).fetchall()
                p['itens'] = [dict(i) for i in itens_rows]
            
            return pedidos
        except Exception as e:
            print(f"Erro no Repo Pedido (Histórico): {e}") # Debug no terminal
            raise e
        finally:
            conn.close()

    def listar_todos(self):
        """Para o Admin"""
        conn = get_db_connection()
        try:
            query = """
                SELECT p.id, p.total, p.status, p.endereco_entrega, p.data_pedido,
                       u.nome_completo as cliente_nome
                FROM pedidos p
                JOIN usuarios u ON p.cliente_id = u.id
                ORDER BY p.id DESC
            """
            rows = conn.execute(query).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()

    def atualizar_status(self, pedido_id, novo_status):
        conn = get_db_connection()
        try:
            conn.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()