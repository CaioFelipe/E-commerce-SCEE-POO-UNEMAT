class ApiClient {
    constructor() {
        this.baseUrl = "http://127.0.0.1:5000/api";
    }

    _getToken() {
        return localStorage.getItem('token');
    }

    async _request(endpoint, method = 'GET', body = null) {
        const headers = {
            'Content-Type': 'application/json'
        };

        // Injeção Automática do Token (Se existir)
        const token = this._getToken();
        if (token) {
            const cleanToken = token.replace(/"/g, ''); 
            headers['Authorization'] = `Bearer ${cleanToken}`;
        }

        const config = {
            method,
            headers
        };

        if (body) {
            config.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, config);
            
            // Tenta fazer o parse do JSON
            let data;
            try {
                data = await response.json();
            } catch (e) {
                data = null;
            }

            // Tratamento Global de Erros (ex: Token Expirado)
            if (response.status === 401) {
                console.warn("Token expirado ou inválido. Realizando logout forçado.");
                localStorage.removeItem('token');
                localStorage.removeItem('usuario');
                window.location.reload(); // Ou redirecionar para login
                throw new Error("Sessão expirada");
            }

            if (!response.ok) {
                // Lança o erro vindo da API (ex: "Estoque insuficiente")
                throw new Error(data && data.erro ? data.erro : `Erro ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`Erro na requisição para ${endpoint}:`, error);
            throw error;
        }
    }

    // Métodos Públicos Facilitadores

    async get(endpoint) {
        return this._request(endpoint, 'GET');
    }

    async post(endpoint, body) {
        return this._request(endpoint, 'POST', body);
    }

    async put(endpoint, body) {
        return this._request(endpoint, 'PUT', body);
    }
    
    async delete(endpoint) {
        return this._request(endpoint, 'DELETE');
    }
}

// Expõe uma instância global para ser usada no app.js
const api = new ApiClient();