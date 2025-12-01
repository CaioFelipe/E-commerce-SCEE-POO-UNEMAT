import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Caminho do Banco de Dados
    DB_NAME = "scee_loja.db"
    DB_PATH = os.path.join(BASE_DIR, DB_NAME)
    
    # Chave Secreta para Assinatura de Tokens (Troque isso em produção!)
    SECRET_KEY = "troque-esta-chave-por-algo-aleatorio-e-seguro"
    
    # Configuração de Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limite de 2MB