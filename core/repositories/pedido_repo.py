import sqlite3
from core.database import get_db_connection

class PedidoRepository:
    def criar_pedido_atomico(self, usuario_id, itens_carrinho, total, endereco):
        """
        Executa a transação completa de venda.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            conn.execute("BEGIN TRANSACTION;")

            # 1. Criar o Pedido
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, total, endereco_entrega, status, metodo_pagamento)
                VALUES (?, ?, ?, 'Processando', 'Desconhecido')
            """, (usuario_id, total, endereco))
            
            pedido_id = cursor.lastrowid

            # 2. Processar Itens e Baixar Estoque
            for item in itens_carrinho:
                prod_id = item['produto_id']
                qtd = item['qtd']
                preco = item['preco_unitario']

                # Verifica estoque (Bloqueio otimista via verificação lógica)
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
            raise e
        finally:
            conn.close()

    def listar_todos(self):
        """
        Retorna todos os pedidos com o nome do cliente.
        Usado pelo Painel Administrativo.
        """
        conn = get_db_connection()
        try:
            # JOIN para pegar o nome do cliente em vez do ID
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
        """Atualiza o status (ex: Processando -> Enviado)."""
        conn = get_db_connection()
        try:
            conn.execute("UPDATE pedidos SET status = ? WHERE id = ?", (novo_status, pedido_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()