class Endereco:
    def __init__(self, id, usuario_id, rua, numero, bairro, cidade, estado, cep):
        self.id = id
        self.usuario_id = usuario_id
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"