class ItemPedido:
    def __init__(self, id, pedido_id, produto_id, quantidade, preco_unitario, nome_produto=None):
        self.id = id
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        # REGRA DE NEGÓCIO: Este preço é imutável após a criação do pedido.
        # Representa quanto o cliente pagou NO ATO, independente do valor atual do produto.
        self.preco_unitario = preco_unitario
        
        # Atributo auxiliar para exibição (geralmente vindo de um JOIN no SQL)
        self.nome_produto = nome_produto

    @property
    def subtotal(self):
        """Calcula o valor total deste item (Qtd x Preço Congelado)."""
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"<ItemPedido {self.nome_produto or self.produto_id} - Qtd: {self.quantidade}>"