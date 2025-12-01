class ItemCarrinho:
    def __init__(self, produto_id, quantidade, preco_unitario, nome_produto=None):
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.nome_produto = nome_produto # Útil para exibição no JSON

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

class Carrinho:
    def __init__(self, usuario_id, itens=None):
        self.usuario_id = usuario_id
        self.itens = itens or [] # Lista de objetos ItemCarrinho

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)