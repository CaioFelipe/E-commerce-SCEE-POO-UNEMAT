import re
from core.models.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, id, nome, email, senha_hash, cpf):
        # Chama o construtor da Pai fixando o tipo
        super().__init__(id, nome, email, senha_hash, tipo='cliente')
        self.cpf = cpf

    def obter_permissao_acesso(self):
        """Implementação Polimórfica: Cliente acessa Loja e Minha Conta."""
        return {
            "area": "loja_web",
            "permissoes": ["comprar", "ver_meus_pedidos", "editar_perfil"],
            "dashboard_url": "/minha-conta"
        }

    def validar_cpf(self):
        if not self.cpf: return False
        cpf_limpo = re.sub(r'\D', '', self.cpf)
        if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11: return False
        
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        if resto == 10: resto = 0
        if resto != int(cpf_limpo[9]): return False
        
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        if resto == 10: resto = 0
        if resto != int(cpf_limpo[10]): return False
        return True