from abc import ABC, abstractmethod
import random

class GatewayPagamento(ABC):
    """
    Interface Abstrata (Strategy Pattern).
    Define o contrato que todo método de pagamento deve seguir.
    """
    @abstractmethod
    def processar_pagamento(self, valor, dados_pagamento=None):
        pass

class PagamentoPix(GatewayPagamento):
    def processar_pagamento(self, valor, dados_pagamento=None):
        # Lógica específica do PIX (ex: validar chave, gerar QR Code)
        print(f"[PIX] Processando pagamento de R$ {valor:.2f}...")
        
        # Simulação: 90% de chance de sucesso
        if random.random() > 0.1:
            return True, "Pagamento via PIX confirmado instantaneamente."
        return False, "Falha na comunicação com o banco central."

class PagamentoCartao(GatewayPagamento):
    def processar_pagamento(self, valor, dados_pagamento=None):
        # Lógica específica de Cartão (ex: validar Luhn, conectar Cielo/Stripe)
        cartao = dados_pagamento.get('numero_cartao', '****')
        print(f"[CARTÃO] Processando R$ {valor:.2f} no cartão final {str(cartao)[-4:]}...")
        
        # Simulação: Validação simples
        if valor > 10000:
            return False, "Valor acima do limite do cartão."
        return True, "Transação de cartão aprovada pela operadora."

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