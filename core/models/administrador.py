from core.models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id, nome, email, senha_hash):
        super().__init__(id, nome, email, senha_hash, tipo='admin')

    def obter_permissao_acesso(self):
        """Implementação Polimórfica: Admin acessa Painel de Gestão."""
        return {
            "area": "gestao_desktop",
            "permissoes": ["gerenciar_produtos", "gerenciar_pedidos", "relatorios_financeiros"],
            "dashboard_url": "/admin/dashboard"
        }
    
    @property
    def tem_acesso_total(self):
        return True