from flask import Blueprint, request, jsonify
from services.catalogo_service import CatalogoService
from services.vendas_service import VendasService
from core.models.cliente import Cliente
from core.models.usuario import Usuario
from core.repositories.usuario_repo import UsuarioRepository
from .utils import token_required
from core.repositories.endereco_repo import EnderecoRepository

api_web_bp = Blueprint('api_web', __name__)

@api_web_bp.route('/produtos', methods=['GET'])
def listar_catalogo():
    service = CatalogoService()
    try:
        produtos = service.listar_produtos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao buscar produtos.'}), 500

@api_web_bp.route('/checkout', methods=['POST'])
@token_required
def finalizar_pedido(current_user):
    data = request.get_json()
    service = VendasService()
    
    try:
        pedido_id = service.realizar_checkout(
            usuario_id=current_user.id,
            dados_checkout=data
        )
        return jsonify({'mensagem': 'Pedido realizado com sucesso!', 'pedido_id': pedido_id}), 201
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 409
    except Exception as e:
        return jsonify({'erro': 'Erro interno ao processar pedido.'}), 500

@api_web_bp.route('/cadastro', methods=['POST'])
def cadastrar_cliente():
    data = request.get_json()
    repo = UsuarioRepository()
    
    if not all(key in data for key in ['nome', 'email', 'senha', 'cpf']):
        return jsonify({'erro': 'Todos os campos são obrigatórios.'}), 400

    if repo.buscar_por_email(data['email']):
        return jsonify({'erro': 'E-mail já cadastrado.'}), 409

    try:
        senha_hash = Usuario.gerar_hash(data['senha'])
        novo_cliente = Cliente(
            id=None,
            nome=data['nome'],
            email=data['email'],
            senha_hash=senha_hash,
            cpf=data['cpf']
        )
        
        if not novo_cliente.validar_cpf():
            return jsonify({'erro': 'CPF inválido.'}), 400

        repo.criar(novo_cliente)
        return jsonify({'mensagem': 'Cadastro realizado com sucesso! Faça login.'}), 201
    except Exception as e:
        return jsonify({'erro': f'Erro ao cadastrar: {str(e)}'}), 500

# --- NOVAS ROTAS DE PERFIL ---

@api_web_bp.route('/perfil', methods=['GET'])
@token_required
def obter_perfil(current_user):
    """Retorna dados do usuário + Endereço salvo."""
    
    # Busca endereço salvo
    endereco_repo = EnderecoRepository()
    end_salvo = endereco_repo.buscar_por_usuario(current_user.id)
    
    return jsonify({
        "id": current_user.id,
        "nome": current_user.nome,
        "email": current_user.email,
        "tipo": current_user.tipo,
        "cpf": getattr(current_user, 'cpf', None),
        "endereco": end_salvo # Retorna {rua, numero, bairro} ou None
    }), 200

@api_web_bp.route('/perfil', methods=['PUT'])
@token_required
def atualizar_perfil(current_user):
    """Permite alterar nome e email."""
    data = request.get_json()
    repo = UsuarioRepository()
    
    if 'nome' in data:
        current_user.nome = data['nome']
    if 'email' in data:
        # Verificar se email já existe (se for diferente do atual)
        if data['email'] != current_user.email:
            existente = repo.buscar_por_email(data['email'])
            if existente:
                return jsonify({'erro': 'E-mail já está em uso por outro usuário.'}), 409
        current_user.email = data['email']
        
    try:
        repo.atualizar(current_user)
        return jsonify({'mensagem': 'Perfil atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar perfil.'}), 500