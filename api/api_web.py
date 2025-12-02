from flask import Blueprint, request, jsonify
import traceback
from services.catalogo_service import CatalogoService
from services.vendas_service import VendasService
from core.models.cliente import Cliente
from core.models.usuario import Usuario
from core.repositories.usuario_repo import UsuarioRepository
from core.repositories.pedido_repo import PedidoRepository
from core.repositories.endereco_repo import EnderecoRepository
from core.repositories.produto_repo import ProdutoRepository 
from .utils import token_required

api_web_bp = Blueprint('api_web', __name__)

@api_web_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    """Retorna lista de categorias para o filtro."""
    repo = ProdutoRepository()
    return jsonify(repo.listar_categorias()), 200

@api_web_bp.route('/produtos', methods=['GET'])
def listar_catalogo():
    repo_prod = ProdutoRepository()
    
    # --- CORREÇÃO AQUI ---
    # O frontend envia ?categoria_id=1, então temos de ler 'categoria_id'
    filtros = {
        'min_price': request.args.get('min_price'),
        'max_price': request.args.get('max_price'),
        'termo': request.args.get('busca'),
        'categoria_id': request.args.get('categoria_id') # Corrigido de 'categoria' para 'categoria_id'
    }
    
    try:
        produtos = repo_prod.listar_todos(filtros)
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@api_web_bp.route('/meus-pedidos', methods=['GET'])
@token_required
def meus_pedidos(current_user):
    repo_pedidos = PedidoRepository()
    try:
        historico = repo_pedidos.buscar_historico_cliente(current_user.id)
        return jsonify(historico), 200
    except Exception as e:
        print(f"ERRO API MEUS PEDIDOS: {e}")
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500

@api_web_bp.route('/checkout', methods=['POST'])
@token_required
def finalizar_pedido(current_user):
    data = request.get_json()
    service = VendasService()
    try:
        pedido_id = service.realizar_checkout(current_user.id, data)
        return jsonify({'mensagem': 'Pedido realizado com sucesso!', 'pedido_id': pedido_id}), 201
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 409
    except Exception as e:
        print(f"Erro checkout: {e}")
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
        novo_cliente = Cliente(None, data['nome'], data['email'], senha_hash, data['cpf'])
        if not novo_cliente.validar_cpf(): return jsonify({'erro': 'CPF inválido.'}), 400
        repo.criar(novo_cliente)
        return jsonify({'mensagem': 'Cadastro realizado com sucesso! Faça login.'}), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@api_web_bp.route('/perfil', methods=['GET'])
@token_required
def obter_perfil(current_user):
    endereco_repo = EnderecoRepository()
    end_salvo = endereco_repo.buscar_por_usuario(current_user.id)
    return jsonify({
        "id": current_user.id, "nome": current_user.nome, "email": current_user.email,
        "tipo": current_user.tipo, "cpf": getattr(current_user, 'cpf', None), "endereco": end_salvo
    }), 200

@api_web_bp.route('/perfil', methods=['PUT'])
@token_required
def atualizar_perfil(current_user):
    data = request.get_json()
    repo = UsuarioRepository()
    if 'nome' in data: current_user.nome = data['nome']
    if 'email' in data: current_user.email = data['email']
    try:
        repo.atualizar(current_user)
        return jsonify({'mensagem': 'Perfil atualizado com sucesso!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500