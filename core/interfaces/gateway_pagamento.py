from abc import ABC, abstractmethod

class GatewayPagamento(ABC):
    """
    Interface Abstrata (Strategy Pattern).
    Define o contrato que todo método de pagamento deve seguir.
    """
    @abstractmethod
    def processar_pagamento(self, valor, dados_pagamento=None):
        pass