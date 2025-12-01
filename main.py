import os
from flask import Flask, send_from_directory
from flask_cors import CORS  # Importação Nova
from config import Config

# Importação dos Blueprints
from api.api_web import api_web_bp
from api.api_gestao import api_gestao_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Habilita CORS para todas as rotas (Permite acesso do Frontend Web)
    CORS(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Registro de Rotas
    app.register_blueprint(api_web_bp, url_prefix='/api/web')
    app.register_blueprint(api_gestao_bp, url_prefix='/api/gestao')

    @app.route('/')
    def index():
        return {"status": "online", "sistema": "SCEE V2 - Polimórfico"}

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)