# services/catalogo_service.py
from core.repositories.produto_repo import ProdutoRepository
from core.models.produto import Produto

class CatalogoService:
    def __init__(self):
        self.repo = ProdutoRepository()

    def listar_produtos(self):
        """Retorna a lista de produtos (Pode incluir lógica de cache aqui no futuro)."""
        return self.repo.listar_todos()

    def buscar_produto(self, produto_id):
        """Busca um único produto e valida se existe."""
        produto = self.repo.buscar_por_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")
        return produto

    def criar_produto(self, dados_produto):
        """
        Recebe um dicionário (vindo do JSON/Tkinter), valida e persiste.
        dados_produto: dict com chaves 'sku', 'nome', 'preco', 'estoque', 'descricao'
        """
        # Validação de Negócio: Preço não pode ser negativo
        if float(dados_produto['preco']) < 0:
            raise ValueError("O preço do produto não pode ser negativo.")

        # Criação da Entidade
        novo_produto = Produto(
            id=None,
            sku=dados_produto['sku'],
            nome=dados_produto['nome'],
            preco=float(dados_produto['preco']),
            estoque=int(dados_produto['estoque'])
        )
        novo_produto.descricao = dados_produto.get('descricao', '')
        novo_produto.imagem_url = dados_produto.get('imagem_url')

        # Persistência
        return self.repo.salvar(novo_produto)