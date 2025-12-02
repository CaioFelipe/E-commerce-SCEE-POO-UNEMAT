from .gateway_pagamento import GatewayPagamento

class PagamentoCartao(GatewayPagamento):
    def processar_pagamento(self, valor, dados_pagamento=None):
        # Lógica específica de Cartão
        cartao = dados_pagamento.get('numero_cartao', '****')
        print(f"[CARTÃO] Processando R$ {valor:.2f} no cartão final {str(cartao)[-4:]}...")
        
        # Simulação: Validação simples de limite
        if valor > 10000:
            return False, "Valor acima do limite do cartão."
        return True, "Transação de cartão aprovada pela operadora."