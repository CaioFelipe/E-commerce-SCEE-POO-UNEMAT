class ItemCarrinho:
    def __init__(self, produto_id, quantidade, preco_unitario, nome_produto=None):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.nome_produto = nome_produto # Útil para exibição no JSON

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
    
    def to_dict(self):
        """Helper para serialização JSON."""
        return {
            "produto_id": self.produto_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "nome_produto": self.nome_produto,
            "subtotal": self.subtotal
        }