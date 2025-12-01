import jwt
import datetime
from config import Config
from core.repositories.usuario_repo import UsuarioRepository

class AuthService:
    def __init__(self):
        self.repo = UsuarioRepository()

    def login(self, email, senha_plana):
        usuario = self.repo.buscar_por_email(email)
        
        if usuario and usuario.verificar_senha(senha_plana):
            # Payload do Token
            # CORREÇÃO: Converter o ID para string para evitar erros de 'Subject must be a string'
            payload = {
                'sub': str(usuario.id), 
                'nome': usuario.nome,
                'tipo': usuario.tipo,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }
            
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            
            # POLIMORFISMO: Chamamos o método abstrato implementado
            dados_acesso = usuario.obter_permissao_acesso()
            
            return {
                "token": token,
                "usuario": {
                    "id": usuario.id,
                    "nome": usuario.nome,
                    "tipo": usuario.tipo,
                    "acesso": dados_acesso
                }
            }
            
        return None