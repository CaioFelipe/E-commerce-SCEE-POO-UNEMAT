from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.catalogo_service import CatalogoService
from core.repositories.pedido_repo import PedidoRepository
from core.repositories.produto_repo import ProdutoRepository  
from core.repositories.usuario_repo import UsuarioRepository  
from .utils import token_required, admin_required

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
    repo = PedidoRepository()
    try:
        pedidos = repo.listar_todos() 
        return jsonify(pedidos), 200
    except Exception:
        return jsonify({'erro': 'Erro ao listar pedidos'}), 500

@api_gestao_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
@token_required
@admin_required
def obter_pedido_detalhado(current_user, pedido_id):
    """Retorna detalhes completos de um pedido específico."""
    repo = PedidoRepository()
    pedido = repo.buscar_por_id_com_itens(pedido_id)
    
    if pedido:
        return jsonify(pedido), 200
    return jsonify({'erro': 'Pedido não encontrado'}), 404

@api_gestao_bp.route('/pedidos/<int:pedido_id>/status', methods=['PUT'])
@token_required
@admin_required
def atualizar_status(current_user, pedido_id):
    """Endpoint para Ana despachar pedido (ADM07)."""
    data = request.get_json()
    repo = PedidoRepository()
    
    sucesso = repo.atualizar_status(pedido_id, data['status'])
    if sucesso:
        return jsonify({'mensagem': 'Status atualizado!'}), 200
    return jsonify({'erro': 'Falha ao atualizar'}), 400

# --- NOVAS ROTAS (CLIENTES, ESTOQUE, CATEGORIAS) ---

@api_gestao_bp.route('/clientes', methods=['GET'])
@token_required
@admin_required
def listar_clientes_rota(current_user):
    repo = UsuarioRepository()
    return jsonify(repo.listar_clientes()), 200

@api_gestao_bp.route('/clientes/<int:cliente_id>/pedidos', methods=['GET'])
@token_required
@admin_required
def historico_cliente_admin(current_user, cliente_id):
    """Reutiliza o repo de pedidos para ver o histórico de um cliente específico."""
    repo = PedidoRepository()
    try:
        historico = repo.buscar_historico_cliente(cliente_id)
        return jsonify(historico), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@api_gestao_bp.route('/categorias', methods=['GET'])
@token_required
@admin_required
def listar_categorias_admin(current_user):
    """Necessário para preencher o Combobox do Desktop."""
    repo = ProdutoRepository()
    return jsonify(repo.listar_categorias()), 200

@api_gestao_bp.route('/produtos', methods=['GET'])
@token_required
@admin_required
def listar_produtos_admin(current_user):
    """Lista produtos para o estoque (aceita filtros igual web)."""
    repo = ProdutoRepository()
    # Pega filtros da query string
    filtros = {
        'termo': request.args.get('termo'),
        'categoria_id': request.args.get('categoria_id')
    }
    return jsonify(repo.listar_todos(filtros)), 200

@api_gestao_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
@token_required
@admin_required
def atualizar_produto(current_user, produto_id):
    """Edição de produto no Estoque."""
    data = request.get_json()
    repo = ProdutoRepository()
    
    # Busca produto existente para garantir que existe
    produto = repo.buscar_por_id(produto_id)
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
        
    # Atualiza campos
    produto.nome = data.get('nome', produto.nome)
    produto.sku = data.get('sku', produto.sku)
    produto.preco = float(data.get('preco', produto.preco))
    produto.estoque = int(data.get('estoque', produto.estoque))
    produto.descricao = data.get('descricao', produto.descricao)
    produto.imagem_url = data.get('imagem_url', produto.imagem_url)
    
    # Se vier categoria, tem que tratar
    if 'categoria_id' in data:
        produto.categoria_id = int(data['categoria_id'])

    try:
        repo.salvar(produto)
        return jsonify({'mensagem': 'Produto atualizado!'}), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

# Rota de Upload (Já existia, mantendo para referência)
@api_gestao_bp.route('/upload', methods=['POST'])
@token_required
@admin_required
def upload_imagem(current_user):
    import os
    from werkzeug.utils import secure_filename
    from flask import current_app
    
    if 'file' not in request.files: return jsonify({'erro': 'Nenhum arquivo'}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({'erro': 'Sem seleção'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        import time
        filename = f"{int(time.time())}_{filename}"
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({'mensagem': 'OK', 'filename': filename}), 201