import requests

class BridgeController:
    """
    Responsável por fazer a comunicação HTTP entre o Tkinter e a API Flask.
    Gerencia o Token JWT e as requisições REST.
    """
    BASE_URL = "http://127.0.0.1:5000/api/gestao"

    def __init__(self):
        self.token = None
        self.usuario_atual = None

    def _get_headers(self):
        """Retorna os cabeçalhos com o Token JWT se estiver logado."""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def login(self, email, senha):
        """
        Envia credenciais para obter o Token JWT.
        """
        try:
            url = f"{self.BASE_URL}/login"
            response = requests.post(url, json={"email": email, "senha": senha})
            
            # Tenta ler o JSON. Se falhar, captura o erro para não travar o app.
            try:
                data = response.json()
            except ValueError:
                # Se não for JSON, provavelmente é um erro HTML do servidor (500 ou 404)
                print(f"ERRO CRÍTICO DO SERVIDOR (Raw Response): {response.text}")
                return False, f"Erro interno do servidor (Status {response.status_code}). Veja o terminal."

            if response.status_code == 200:
                self.token = data.get("token")
                self.usuario_atual = data.get("usuario")
                return True, "Login realizado com sucesso!"
            else:
                return False, data.get("erro", "Falha no login")

        except requests.exceptions.ConnectionError:
            return False, "Erro: Não foi possível conectar ao servidor. Verifique se o main.py está rodando."
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    def listar_pedidos(self):
        """Busca lista de pedidos para a Ana gerenciar (RF08)."""
        if not self.token:
            return []
        try:
            response = requests.get(f"{self.BASE_URL}/pedidos", headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []

    def atualizar_status_pedido(self, pedido_id, novo_status):
        """Atualiza status para 'Enviado' (ADM07)."""
        url = f"{self.BASE_URL}/pedidos/{pedido_id}/status"
        payload = {"status": novo_status}
        try:
            response = requests.put(url, json=payload, headers=self._get_headers())
            return response.status_code == 200
        except:
            return False

    def criar_produto(self, produto_data):
        """Envia dados do novo produto (RF04)."""
        url = f"{self.BASE_URL}/produtos"
        try:
            response = requests.post(url, json=produto_data, headers=self._get_headers())
            return response.status_code == 201
        except:
            return False

    def enviar_imagem(self, caminho_arquivo):
        """
        Lê o arquivo do disco local e faz upload para a API.
        Retorna o nome final do arquivo salvo no servidor.
        """
        url = f"{self.BASE_URL}/upload"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            with open(caminho_arquivo, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, headers=headers, files=files)
                
            if response.status_code == 201:
                return True, response.json()['filename']
            else:
                # Proteção contra erros não-JSON no upload também
                try:
                    erro_msg = response.json().get('erro', 'Falha no upload')
                except:
                    erro_msg = f"Erro servidor: {response.status_code}"
                return False, erro_msg
        except Exception as e:
            return False, str(e)
