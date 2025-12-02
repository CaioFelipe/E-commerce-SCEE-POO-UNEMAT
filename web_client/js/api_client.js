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

        const token = this._getToken();
        if (token) {
            // Remove aspas extras caso existam
            const cleanToken = token.replace(/"/g, '');
            headers['Authorization'] = `Bearer ${cleanToken}`;
        }

        const config = { method, headers };

        if (body) {
            config.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, config);
            
            let data;
            try {
                data = await response.json();
            } catch (e) {
                data = null;
            }

            // CORREÇÃO CRÍTICA:
            // Só faz logout forçado (reload) se for erro 401 E NÃO FOR TENTATIVA DE LOGIN.
            // Se for login (endpoint contém 'login'), deixamos o app.js tratar o erro (ex: "Senha incorreta").
            if (response.status === 401 && !endpoint.includes('login')) {
                console.warn("Sessão expirada. Realizando logout.");
                localStorage.removeItem('token');
                localStorage.removeItem('usuario');
                window.location.reload(); 
                throw new Error("Sessão expirada");
            }

            if (!response.ok) {
                throw new Error(data && data.erro ? data.erro : `Erro ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`Erro requisição ${endpoint}:`, error);
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