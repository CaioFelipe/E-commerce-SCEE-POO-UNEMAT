from abc import ABC, abstractmethod
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

class Usuario(ABC):
    """
    Classe Base Abstrata.
    Não pode ser instanciada diretamente (ex: u = Usuario(...)).
    Define o contrato que Cliente e Administrador devem seguir.
    """
    def __init__(self, id, nome, email, senha_hash, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.tipo = tipo

    @staticmethod
    def gerar_hash(senha_plana):
        return ph.hash(senha_plana)

    def verificar_senha(self, senha_plana):
        try:
            return ph.verify(self.senha_hash, senha_plana)
        except VerifyMismatchError:
            return False

    @abstractmethod
    def obter_permissao_acesso(self):
        """
        Método Polimórfico (Abstrato).
        Cada filha DEVE implementar sua própria versão.
        Retorna um dicionário ou string descrevendo onde o usuário pode entrar.
        """
        pass