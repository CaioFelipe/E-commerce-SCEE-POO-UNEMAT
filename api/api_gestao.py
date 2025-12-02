from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.catalogo_service import CatalogoService
from core.repositories.pedido_repo import PedidoRepository
from .utils import token_required, admin_required
import os
from werkzeug.utils import secure_filename
from flask import current_app

api_gestao_bp = Blueprint('api_gestao', __name__)

@api_gestao_bp.route('/login', methods=['POST'])
def login():
    """Realiza a autenticação e retorna o JWT."""
    data = request.get_json()
    auth_service = AuthService()
    
    # O Service já encapsula a lógica de Hash e geração de Token
    resultado = auth_service.login(data.get('email'), data.get('senha'))
    
    if resultado:
        return jsonify(resultado), 200
    return jsonify({'erro': 'Credenciais inválidas'}), 401

@api_gestao_bp.route('/produtos', methods=['POST'])
@token_required
@admin_required
def criar_produto(current_user):
    """Endpoint para Ana cadastrar produtos (RF04)."""
    data = request.get_json()
    service = CatalogoService()
    
    try:
        # O Service valida preço negativo e persiste
        novo_produto = service.criar_produto(data)
        return jsonify({'mensagem': 'Produto criado com sucesso!', 'id': novo_produto.id}), 201
    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno ao criar produto.'}), 500

@api_gestao_bp.route('/pedidos', methods=['GET'])
@token_required
@admin_required
def listar_pedidos(current_user):
    """Endpoint para listar pedidos para processamento (RF08)."""
    # Mantendo Repo direto pois VendasService focou no Checkout
    repo = PedidoRepository()
    try:
        pedidos = repo.listar_todos() 
        return jsonify(pedidos), 200
    except Exception:
        return jsonify({'erro': 'Erro ao listar pedidos'}), 500

@api_gestao_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
@token_required
@admin_required
def atualizar_status(current_user, pedido_id):
    """Endpoint para Ana despachar pedido (ADM07)."""
    data = request.get_json()
    repo = PedidoRepository()
    
    # Assumindo que implementaremos 'atualizar_status' no repo na Fase de Polimento
    # ou usando um método SQL direto se necessário
    if not hasattr(repo, 'atualizar_status'):
         return jsonify({'erro': 'Método não implementado no Repo ainda'}), 501

    sucesso = repo.atualizar_status(pedido_id, data['status'])
    if sucesso:
        return jsonify({'mensagem': 'Status atualizado!'}), 200
    return jsonify({'erro': 'Falha ao atualizar'}), 400

@api_gestao_bp.route('/upload', methods=['POST'])
@token_required
@admin_required
def upload_imagem(current_user):
    """
    Recebe um arquivo de imagem via Multipart Form-Data.
    Salva na pasta UPLOAD_FOLDER e retorna o nome do arquivo.
    """
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        # Garante nome único para evitar sobrescrita (timestamp simples)
        import time
        filename = f"{int(time.time())}_{filename}"
        
        caminho_completo = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho_completo)
        
        return jsonify({'mensagem': 'Upload realizado!', 'filename': filename}), 201