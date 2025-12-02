from core.database import get_db_connection
from core.models.cliente import Cliente
from core.models.administrador import Administrador

class UsuarioRepository:
    def _instanciar_correto(self, row):
        """Factory interna para instanciar a classe certa."""
        if not row:
            return None
        
        # Converte a row do SQLite para dicionário para evitar erros de índice
        dados = dict(row)
        tipo = dados.get('tipo')
        
        if tipo == 'admin':
            return Administrador(
                id=dados['id'],
                nome=dados['nome_completo'],
                email=dados['email'],
                senha_hash=dados['senha_hash']
            )
        
        elif tipo == 'cliente':
            # Garante leitura segura do CPF
            cpf = dados.get('cpf') 
            return Cliente(
                id=dados['id'],
                nome=dados['nome_completo'],
                email=dados['email'],
                senha_hash=dados['senha_hash'],
                cpf=cpf
            )
            
        return None

    def buscar_por_email(self, email):
        conn = get_db_connection()
        try:
            # JOIN para trazer dados completos (incluindo CPF se houver)
            query = """
                SELECT u.*, c.cpf 
                FROM usuarios u
                LEFT JOIN clientes_info c ON u.id = c.usuario_id
                WHERE u.email = ?
            """
            row = conn.execute(query, (email,)).fetchone()
            return self._instanciar_correto(row)
        finally:
            conn.close()

    def buscar_por_id(self, id):
        conn = get_db_connection()
        try:
            query = """
                SELECT u.*, c.cpf 
                FROM usuarios u
                LEFT JOIN clientes_info c ON u.id = c.usuario_id
                WHERE u.id = ?
            """
            row = conn.execute(query, (id,)).fetchone()
            return self._instanciar_correto(row)
        finally:
            conn.close()

    def criar(self, usuario):
        conn = get_db_connection()
        try:
            cursor = conn.execute("""
                INSERT INTO usuarios (nome_completo, email, senha_hash, tipo)
                VALUES (?, ?, ?, ?)
            """, (usuario.nome, usuario.email, usuario.senha_hash, usuario.tipo))
            usuario.id = cursor.lastrowid
            
            # Se for instância de Cliente, salva o CPF
            if isinstance(usuario, Cliente) and usuario.cpf:
                conn.execute("""
                    INSERT INTO clientes_info (usuario_id, cpf) VALUES (?, ?)
                """, (usuario.id, usuario.cpf))
                
            conn.commit()
            return usuario
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def atualizar(self, usuario):
        """Atualiza dados básicos do usuário."""
        conn = get_db_connection()
        try:
            conn.execute("""
                UPDATE usuarios SET nome_completo = ?, email = ?
                WHERE id = ?
            """, (usuario.nome, usuario.email, usuario.id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def listar_clientes(self):
        """Retorna todos os usuários do tipo 'cliente'."""
        conn = get_db_connection()
        try:
            query = """
                SELECT u.id, u.nome_completo, u.email, u.data_cadastro, c.cpf
                FROM usuarios u
                LEFT JOIN clientes_info c ON u.id = c.usuario_id
                WHERE u.tipo = 'cliente'
                ORDER BY u.nome_completo
            """
            rows = conn.execute(query).fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()