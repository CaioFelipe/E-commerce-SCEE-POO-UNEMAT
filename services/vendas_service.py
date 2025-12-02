from core.repositories.pedido_repo import PedidoRepository
from core.repositories.endereco_repo import EnderecoRepository
from core.interfaces import FabricaPagamento

class VendasService:
    def __init__(self):
        self.pedido_repo = PedidoRepository()
        self.endereco_repo = EnderecoRepository()

    def realizar_checkout(self, usuario_id, dados_checkout):
        itens_carrinho = dados_checkout.get('itens')
        
        # O total que vem do front já deve ser (Produtos + Frete) ou calculamos aqui.
        # Para ser seguro, vamos confiar que o front manda:
        # total_produtos: valor dos itens
        # valor_frete: valor do frete
        # total_final: soma dos dois
        
        valor_frete = float(dados_checkout.get('valor_frete', 0))
        total_final = float(dados_checkout.get('total')) 
        
        end_data = dados_checkout.get('endereco')
        
        if end_data:
            self.endereco_repo.salvar_ou_atualizar(
                usuario_id, 
                end_data['rua'], 
                end_data['numero'], 
                end_data['bairro']
            )

        metodo = dados_checkout.get('metodo_pagamento', 'pix')
        dados_pagamento_extra = dados_checkout.get('dados_pagamento', {}) 

        gateway = FabricaPagamento.criar(metodo)
        # Processa o valor total (incluindo frete)
        pago_sucesso, msg_pagamento = gateway.processar_pagamento(total_final, dados_pagamento_extra)

        if not pago_sucesso:
            raise ValueError(f"Pagamento Recusado: {msg_pagamento}")

        if not itens_carrinho:
            raise ValueError("Carrinho vazio.")

        endereco_str = f"{end_data['rua']}, {end_data['numero']} - {end_data['bairro']}"

        try:
            pedido_id = self.pedido_repo.criar_pedido_atomico(
                usuario_id=usuario_id,
                itens_carrinho=itens_carrinho,
                total=total_final,     # Valor final pago
                endereco=endereco_str,
                valor_frete=valor_frete # Novo campo
            )
            return pedido_id
        except Exception as e:
            print(f"Erro no checkout: {e}")
            raise e