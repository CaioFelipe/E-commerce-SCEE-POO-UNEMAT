from .item_carrinho import ItemCarrinho

class Carrinho:
    def __init__(self, usuario_id, itens=None):
        self.usuario_id = usuario_id
        self.itens = itens or [] # Lista de objetos ItemCarrinho

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)

    def adicionar_item(self, item: ItemCarrinho):
        # Verifica se o item já existe para apenas somar quantidade
        for i in self.itens:
            if i.produto_id == item.produto_id:
                i.quantidade += item.quantidade
                return
        self.itens.append(item)

    def remover_item(self, produto_id):
        self.itens = [i for i in self.itens if i.produto_id != produto_id]

    def limpar(self):
        self.itens = []
    
    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "itens": [item.to_dict() for item in self.itens],
            "total": self.total
        }