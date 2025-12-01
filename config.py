import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Definição do caminho do banco de dados
    DB_NAME = "scee_loja.db"
    DB_PATH = os.path.join(BASE_DIR, DB_NAME)
    
    # Segurança (JWT e Sessões)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-super-secreta-desenvolvimento'
    
    # Configuração de Uploads (Imagens de Produtos)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB conforme RNF04 (Upload)