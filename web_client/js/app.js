let carrinho = [];
let token = localStorage.getItem('token');
let usuario = JSON.parse(localStorage.getItem('usuario'));

document.addEventListener('DOMContentLoaded', () => {
    carregarProdutos();
    atualizarInterfaceAuth();
    atualizarContadorCarrinho();
});

// --- PRODUTOS ---
async function carregarProdutos() {
    const grid = document.getElementById('product-list');
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Carregando catálogo...</p>';
    try {
        const produtos = await api.get('/web/produtos');
        grid.innerHTML = ''; 
        if (produtos.length === 0) {
            grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Nenhum produto disponível.</p>';
            return;
        }
        produtos.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            const imgUrl = p.imagem_url ? `/uploads/${p.imagem_url}` : null;
            const imgTag = imgUrl 
                ? `<img src="${imgUrl}" alt="${p.nome}" onerror="this.src='https://via.placeholder.com/150?text=Sem+Imagem'">`
                : `<img src="https://via.placeholder.com/150?text=Sem+Imagem" alt="${p.nome}">`;

            card.innerHTML = `
                ${imgTag}
                <h3>${p.nome}</h3>
                <div class="stock">Estoque: ${p.estoque} un.</div>
                <div class="price">R$ ${p.preco.toFixed(2)}</div>
                <button class="btn-add" 
                    ${p.estoque > 0 ? '' : 'disabled style="background-color:#555;cursor:not-allowed;"'}
                    onclick="adicionarAoCarrinho(${p.id}, '${p.nome.replace(/'/g, "\\'")}', ${p.preco})">
                    ${p.estoque > 0 ? 'Adicionar' : 'Indisponível'}
                </button>
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error(error);
        grid.innerHTML = `<p style="color: var(--danger-color); text-align: center;">Erro: ${error.message}</p>`;
    }
}

// --- CARRINHO ---
function adicionarAoCarrinho(id, nome, preco) {
    const itemExistente = carrinho.find(item => item.produto_id === id);
    if (itemExistente) {
        itemExistente.qtd += 1;
    } else {
        carrinho.push({ produto_id: id, nome: nome, preco_unitario: preco, qtd: 1 });
    }
    atualizarContadorCarrinho();
    const btnCart = document.getElementById('btn-cart');
    btnCart.style.color = 'var(--success-color)';
    setTimeout(() => btnCart.style.color = '', 500);
}

function atualizarContadorCarrinho() {
    const totalItens = carrinho.reduce((acc, item) => acc + item.qtd, 0);
    document.getElementById('cart-count').innerText = totalItens;
}

function renderizarCarrinho() {
    const container = document.getElementById('cart-items');
    container.innerHTML = '';
    let total = 0;
    if (carrinho.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #777;">Vazio.</p>';
        document.getElementById('btn-checkout-start').style.display = 'none';
        document.getElementById('checkout-form').classList.add('hidden');
    } else {
        document.getElementById('btn-checkout-start').style.display = 'block';
        carrinho.forEach((item, index) => {
            const subtotal = item.qtd * item.preco_unitario;
            total += subtotal;
            container.innerHTML += `
                <div class="cart-item">
                    <span>${item.qtd}x ${item.nome}</span>
                    <div>
                        <span style="font-weight: bold; margin-right: 10px;">R$ ${subtotal.toFixed(2)}</span>
                        <button onclick="removerDoCarrinho(${index})" style="background:none; border:none; color:var(--danger-color); cursor:pointer;">&times;</button>
                    </div>
                </div>
            `;
        });
    }
    document.getElementById('cart-total').innerText = total.toFixed(2);
}

function removerDoCarrinho(index) {
    carrinho.splice(index, 1);
    renderizarCarrinho();
    atualizarContadorCarrinho();
}

async function iniciarCheckout() {
    if (!token) {
        alert("Faça login para continuar.");
        toggleCart();
        toggleLogin();
        return;
    }

    // Mostra o formulário
    document.getElementById('checkout-area').classList.remove('hidden');
    document.getElementById('btn-checkout-start').classList.add('hidden');

    // Tenta preencher o endereço automaticamente (Persistência)
    try {
        const perfil = await api.get('/web/perfil');
        if (perfil.endereco) {
            document.getElementById('end-rua').value = perfil.endereco.rua || '';
            document.getElementById('end-num').value = perfil.endereco.numero || '';
            document.getElementById('end-bairro').value = perfil.endereco.bairro || '';
        }
    } catch (e) {
        console.log("Sem endereço salvo.");
    }
}

function togglePagamento() {
    const metodo = document.querySelector('input[name="pagamento"]:checked').value;
    const divCartao = document.getElementById('div-cartao');
    if (metodo === 'cartao') {
        divCartao.classList.remove('hidden');
    } else {
        divCartao.classList.add('hidden');
    }
}

async function finalizarCompra() {
    // 1. Coleta Endereço
    const rua = document.getElementById('end-rua').value;
    const num = document.getElementById('end-num').value;
    const bairro = document.getElementById('end-bairro').value;

    if (!rua || !num || !bairro) {
        alert("O endereço é obrigatório!");
        return;
    }

    // 2. Coleta Pagamento
    const metodo = document.querySelector('input[name="pagamento"]:checked').value;
    const dadosPagamento = {};
    
    if (metodo === 'cartao') {
        const numCartao = document.getElementById('pag-cartao-num').value;
        if (!numCartao || numCartao.length < 13) {
            alert("Digite um número de cartão válido.");
            return;
        }
        dadosPagamento.numero_cartao = numCartao;
    }

    // 3. Monta Payload
    const total = parseFloat(document.getElementById('cart-total').innerText);
    const payload = {
        itens: carrinho,
        total: total,
        endereco: { rua, numero: num, bairro },
        metodo_pagamento: metodo,
        dados_pagamento: dadosPagamento
    };

    const btn = document.querySelector('#checkout-area button');
    const textoOriginal = btn.innerText;
    btn.innerText = "Processando...";
    btn.disabled = true;

    try {
        const data = await api.post('/web/checkout', payload);
        alert(`Pedido Confirmado com Sucesso!\nID: ${data.pedido_id}\nStatus: Processando`);
        
        // Limpa tudo
        carrinho = [];
        toggleCart();
        atualizarContadorCarrinho();
        carregarProdutos();
    } catch (error) {
        alert(`Falha no Pedido: ${error.message}`);
    } finally {
        btn.innerText = textoOriginal;
        btn.disabled = false;
    }
}

// --- PERFIL ---
async function carregarPerfil() {
    try {
        const perfil = await api.get('/web/perfil');
        document.getElementById('perf-nome').value = perfil.nome;
        document.getElementById('perf-email').value = perfil.email;
        document.getElementById('perf-cpf').value = perfil.cpf || "N/A";
    } catch (e) {
        console.error("Erro ao carregar perfil:", e);
    }
}

async function salvarPerfil() {
    const nome = document.getElementById('perf-nome').value;
    const email = document.getElementById('perf-email').value;

    try {
        const res = await api.put('/web/perfil', { nome, email });
        alert(res.mensagem);
        
        // Atualiza cache local
        usuario.nome = nome;
        usuario.email = email;
        localStorage.setItem('usuario', JSON.stringify(usuario));
        atualizarInterfaceAuth();
        toggleProfile();
    } catch (e) {
        alert(e.message);
    }
}

// --- AUTH ---
async function fazerLogin() {
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-pass').value;
    const errorMsg = document.getElementById('login-error');
    errorMsg.innerText = '';

    if (!email || !senha) return;

    try {
        const data = await api.post('/gestao/login', { email, senha });
        token = data.token;
        usuario = data.usuario;
        localStorage.setItem('token', token);
        localStorage.setItem('usuario', JSON.stringify(usuario));
        toggleLogin();
        atualizarInterfaceAuth();
        document.getElementById('login-email').value = '';
        document.getElementById('login-pass').value = '';
    } catch (error) {
        errorMsg.innerText = error.message;
    }
}

async function fazerCadastro() {
    const nome = document.getElementById('cad-nome').value;
    const email = document.getElementById('cad-email').value;
    const cpf = document.getElementById('cad-cpf').value;
    const senha = document.getElementById('cad-senha').value;
    const senhaConf = document.getElementById('cad-senha-conf').value;
    const errorMsg = document.getElementById('cad-error');

    errorMsg.innerText = '';

    if (!nome || !email || !cpf || !senha) {
        errorMsg.innerText = 'Preencha todos os campos.';
        return;
    }

    if (senha !== senhaConf) {
        errorMsg.innerText = 'As senhas não coincidem!';
        return;
    }

    const btn = document.querySelector('#modal-cadastro button.btn-add');
    btn.innerText = "Enviando...";
    btn.disabled = true;

    try {
        const data = await api.post('/web/cadastro', { nome, email, cpf, senha });
        alert("Conta criada! Faça login.");
        toggleCadastro();
        toggleLogin();
        document.getElementById('cad-nome').value = '';
        document.getElementById('cad-email').value = '';
        document.getElementById('cad-cpf').value = '';
        document.getElementById('cad-senha').value = '';
        document.getElementById('cad-senha-conf').value = '';
    } catch (error) {
        errorMsg.innerText = error.message;
    } finally {
        btn.innerText = "Cadastrar";
        btn.disabled = false;
    }
}

function logout() {
    token = null;
    usuario = null;
    localStorage.clear();
    atualizarInterfaceAuth();
    window.location.reload();
}

function atualizarInterfaceAuth() {
    const userDisplay = document.getElementById('user-display');
    const btnLogin = document.getElementById('btn-login');
    const btnProfile = document.getElementById('btn-profile');
    const btnLogout = document.getElementById('btn-logout');

    if (token && usuario) {
        userDisplay.innerText = `Olá, ${usuario.nome.split(' ')[0]}`;
        userDisplay.classList.remove('hidden');
        btnLogin.classList.add('hidden');
        btnProfile.classList.remove('hidden');
        btnLogout.classList.remove('hidden');
    } else {
        userDisplay.classList.add('hidden');
        btnLogin.classList.remove('hidden');
        btnProfile.classList.add('hidden');
        btnLogout.classList.add('hidden');
    }
}

// --- TOGGLES ---
function toggleLogin() { document.getElementById('modal-login').classList.toggle('hidden'); }
function toggleCadastro() { document.getElementById('modal-cadastro').classList.toggle('hidden'); }
function toggleCart() { 
    const modal = document.getElementById('modal-cart');
    modal.classList.toggle('hidden');
    
    if(!modal.classList.contains('hidden')) {
        renderizarCarrinho();
    } else {
        // Reseta visualização ao fechar
        document.getElementById('checkout-area').classList.add('hidden');
        document.getElementById('btn-checkout-start').classList.remove('hidden');
    }
}
function toggleProfile() {
    const modal = document.getElementById('modal-profile');
    modal.classList.toggle('hidden');
    if(!modal.classList.contains('hidden')) carregarPerfil();
}
function alternarParaCadastro() { toggleLogin(); toggleCadastro(); }
function alternarParaLogin() { toggleCadastro(); toggleLogin(); }