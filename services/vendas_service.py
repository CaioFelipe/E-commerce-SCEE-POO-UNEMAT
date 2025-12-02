from core.repositories.pedido_repo import PedidoRepository
from core.repositories.endereco_repo import EnderecoRepository
from core.interfaces import FabricaPagamento

class VendasService:
    def __init__(self):
        self.pedido_repo = PedidoRepository()
        self.endereco_repo = EnderecoRepository()

    def realizar_checkout(self, usuario_id, dados_checkout):
        itens_carrinho = dados_checkout.get('itens')
        total_calculado = dados_checkout.get('total')
        end_data = dados_checkout.get('endereco') # Dict {rua, numero, bairro}
        
        # 1. Salvar Endereço para o Futuro (Persistência)
        if end_data:
            self.endereco_repo.salvar_ou_atualizar(
                usuario_id, 
                end_data['rua'], 
                end_data['numero'], 
                end_data['bairro']
            )

        # 2. Processamento de Pagamento (Polimorfismo)
        metodo = dados_checkout.get('metodo_pagamento', 'pix')
        dados_pagamento_extra = dados_checkout.get('dados_pagamento', {}) # Ex: numero cartao

        gateway = FabricaPagamento.criar(metodo)
        pago_sucesso, msg_pagamento = gateway.processar_pagamento(total_calculado, dados_pagamento_extra)

        if not pago_sucesso:
            raise ValueError(f"Pagamento Recusado: {msg_pagamento}")

        # 3. Validação e Criação do Pedido
        if not itens_carrinho:
            raise ValueError("Carrinho vazio.")

        endereco_str = f"{end_data['rua']}, {end_data['numero']} - {end_data['bairro']}"

        try:
            pedido_id = self.pedido_repo.criar_pedido_atomico(
                usuario_id=usuario_id,
                itens_carrinho=itens_carrinho,
                total=total_calculado,
                endereco=endereco_str
            )
            return pedido_id
        except Exception as e:
            print(f"Erro no checkout: {e}")
            raise e