from datetime import datetime

class Pedido:
    # Definição de constantes para evitar "strings mágicas" no código
    STATUS_PROCESSANDO = 'Processando'
    STATUS_ENVIADO = 'Enviado'
    STATUS_CANCELADO = 'Cancelado'

    def __init__(self, id, cliente_id, data_pedido, total, endereco_entrega, status=STATUS_PROCESSANDO, itens=None):
        self.id = id
        self.cliente_id = cliente_id
        
        # Garante que data_pedido seja um objeto datetime, mesmo vindo string do banco
        if isinstance(data_pedido, str):
            self.data_pedido = datetime.fromisoformat(data_pedido)
        else:
            self.data_pedido = data_pedido or datetime.now()
            
        self.total = total
        self.endereco_entrega = endereco_entrega
        self.status = status
        self.itens = itens or [] # Lista de objetos ItemPedido

    def pode_ser_cancelado(self):
        """
        Regra de Negócio: Apenas pedidos que ainda não foram enviados podem ser cancelados.
        Atende à necessidade da Ana de gerenciar desistências[cite: 489].
        """
        return self.status == self.STATUS_PROCESSANDO

    def __repr__(self):
        return f"<Pedido #{self.id} - Cliente: {self.cliente_id} - Status: {self.status}>"