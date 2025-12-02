from .pagamento_pix import PagamentoPix
from .pagamento_cartao import PagamentoCartao

class FabricaPagamento:
    """
    Factory Pattern simples para instanciar a classe certa baseada numa string.
    """
    @staticmethod
    def criar(tipo):
        if tipo == 'pix':
            return PagamentoPix()
        elif tipo == 'cartao':
            return PagamentoCartao()
        else:
            raise ValueError(f"Método de pagamento '{tipo}' não suportado.")