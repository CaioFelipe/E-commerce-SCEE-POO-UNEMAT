class Produto:
    def __init__(self, id, sku, nome, preco, estoque):
        self.id = id
        self.sku = sku
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def verificar_disponibilidade(self, quantidade_solicitada):
        """Retorna True se houver estoque suficiente."""
        return self.estoque >= quantidade_solicitada

    def baixar_estoque(self, quantidade):
        """
        Abate do estoque.
        Lança erro se tentar deixar negativo (Regra de Negócio Crítica).
        """
        if not self.verificar_disponibilidade(quantidade):
            raise ValueError(f"Estoque insuficiente para o produto {self.nome}")
        self.estoque -= quantidade