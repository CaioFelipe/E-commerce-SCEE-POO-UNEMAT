from functools import wraps
from flask import request, jsonify, current_app
import jwt
import traceback
from core.repositories.usuario_repo import UsuarioRepository
from core.models.administrador import Administrador

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # print("\n--- INÍCIO AUTENTICAÇÃO ---") # Comentado para poluir menos, descomente se precisar
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token ausente!'}), 401
        
        try:
            # Decodifica
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            
            user_id = data['sub']
            
            # Repositório
            repo = UsuarioRepository()
            current_user = repo.buscar_por_id(user_id)
            
            if not current_user:
                print(f"ERRO AUTH: Usuário ID {user_id} não encontrado.")
                raise Exception("Usuário não encontrado")
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError as e:
            print(f"ERRO TOKEN: {str(e)}")
            return jsonify({'message': 'Token inválido!'}), 401
        except Exception as e:
            print(f"ERRO CRÍTICO AUTH: {str(e)}")
            traceback.print_exc()
            return jsonify({'message': 'Erro interno de autenticação.'}), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not isinstance(current_user, Administrador):
            return jsonify({'message': 'Acesso restrito a administradores!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated