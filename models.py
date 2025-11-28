class Produto:
    """
    Representa a entidade Produto conforme especificação[cite: 428].
    """
    def __init__(self, id, nome, sku, descricao, preco, imagem_url, estoque):
        self.id = id
        self.nome = nome
        self.sku = sku
        self.descricao = descricao
        self.preco = preco
        self.imagem_url = imagem_url
        self.estoque = estoque

    def formatar_preco(self):
        return f"R$ {self.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class Carrinho:
    """
    Gerencia a lógica do Carrinho de Compras[cite: 163, 310].
    """
    def __init__(self):
        self.itens = [] # Lista de dicionários {'produto': Produto, 'quantidade': int}

    def adicionar_item(self, produto, quantidade=1):
        for item in self.itens:
            if item['produto'].id == produto.id:
                item['quantidade'] += quantidade
                return
        self.itens.append({'produto': produto, 'quantidade': quantidade})

    def remover_item(self, produto_id):
        self.itens = [item for item in self.itens if item['produto'].id != produto_id]

    def calcular_total(self):
        return sum(item['produto'].preco * item['quantidade'] for item in self.itens)
