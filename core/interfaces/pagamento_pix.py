import random
from .gateway_pagamento import GatewayPagamento

class PagamentoPix(GatewayPagamento):
    def processar_pagamento(self, valor, dados_pagamento=None):
        # Lógica específica do PIX
        print(f"[PIX] Processando pagamento de R$ {valor:.2f}...")
        
        # Simulação: 90% de chance de sucesso
        if random.random() > 0.1:
            return True, "Pagamento via PIX confirmado instantaneamente."
        return False, "Falha na comunicação com o banco central."