from abc import ABC, abstractmethod

class BaseRepository(ABC):
    """
    Interface abstrata para garantir que todos os repositórios
    sigam o mesmo padrão de nomenclatura e comportamento.
    """

    @abstractmethod
    def buscar_por_id(self, id):
        """Retorna uma entidade única pelo seu ID."""
        pass

    @abstractmethod
    def listar_todos(self):
        """Retorna uma lista de todas as entidades."""
        pass

    @abstractmethod
    def salvar(self, entidade):
        """
        Insere uma nova entidade ou Atualiza uma existente.
        Deve lidar com a lógica de ID (se tem ID = update, se não tem = insert).
        """
        pass

    @abstractmethod
    def deletar(self, id):
        """Remove uma entidade do banco de dados pelo ID."""
        pass