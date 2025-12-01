import sqlite3
from core.database import get_db_connection

class PedidoRepository:
    def criar_pedido_atomico(self, usuario_id, itens_carrinho, total, endereco):
        """
        Executa a transação completa de venda.
        itens_carrinho: lista de objetos/dicts com {'produto_id': x, 'qtd': y, 'preco_unitario': z}
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # INÍCIO DA TRANSAÇÃO
            conn.execute("BEGIN TRANSACTION;")

            # 1. Criar o Pedido
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, total, endereco_entrega, status)
                VALUES (?, ?, ?, 'Processando')
            """, (usuario_id, total, endereco))
            
            pedido_id = cursor.lastrowid

            # 2. Processar Itens e Baixar Estoque
            for item in itens_carrinho:
                prod_id = item['produto_id']
                qtd = item['qtd']
                preco = item['preco_unitario']

                # Verificação de Concorrência (RNF07.3)
                # Tenta baixar o estoque. Se qtd > estoque, a constraint CHECK do banco falharia,
                # mas é bom verificar logicamente também ou capturar o erro do SQL.
                
                # Vamos verificar o estoque atual no banco dentro da transação
                cursor.execute("SELECT estoque FROM produtos WHERE id = ?", (prod_id,))
                row = cursor.fetchone()
                if not row or row['estoque'] < qtd:
                    raise ValueError(f"Produto ID {prod_id} sem estoque suficiente durante o checkout.")

                # Atualiza Estoque
                cursor.execute("""
                    UPDATE produtos SET estoque = estoque - ? WHERE id = ?
                """, (qtd, prod_id))

                # Insere Item do Pedido
                cursor.execute("""
                    INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario)
                    VALUES (?, ?, ?, ?)
                """, (pedido_id, prod_id, qtd, preco))

            # 3. Limpar Carrinho (Já que virou pedido)
            # Assumindo que temos a lógica para pegar o ID do carrinho, aqui simplificado:
            cursor.execute("DELETE FROM carrinhos WHERE usuario_id = ?", (usuario_id,))

            # COMMIT DA TRANSAÇÃO
            conn.commit()
            return pedido_id

        except Exception as e:
            # ROLLBACK EM CASO DE ERRO (RNF07.1)
            conn.rollback()
            print(f"Erro na transação do pedido: {e}")
            raise e # Repassa o erro para a API tratar (retornar 400/500)
        finally:
            conn.close()