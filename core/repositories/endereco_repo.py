from core.database import get_db_connection

class EnderecoRepository:
    def salvar_ou_atualizar(self, usuario_id, rua, numero, bairro):
        conn = get_db_connection()
        try:
            # Verifica se já existe endereço para este usuário
            cursor = conn.execute("SELECT id FROM enderecos WHERE usuario_id = ?", (usuario_id,))
            existe = cursor.fetchone()

            if existe:
                conn.execute("""
                    UPDATE enderecos SET rua=?, numero=?, bairro=? WHERE usuario_id=?
                """, (rua, numero, bairro, usuario_id))
            else:
                conn.execute("""
                    INSERT INTO enderecos (usuario_id, rua, numero, bairro) VALUES (?, ?, ?, ?)
                """, (usuario_id, rua, numero, bairro))
            conn.commit()
        finally:
            conn.close()

    def buscar_por_usuario(self, usuario_id):
        conn = get_db_connection()
        try:
            row = conn.execute("SELECT * FROM enderecos WHERE usuario_id = ?", (usuario_id,)).fetchone()
            if row:
                return dict(row)
            return None
        finally:
            conn.close()