# Expõe os Blueprints para facilitar a importação no main.py
from .api_web import api_web_bp
from .api_gestao import api_gestao_bp

# Define a lista de módulos que serão importados se alguém usar "from api import *"
__all__ = ['api_web_bp', 'api_gestao_bp']