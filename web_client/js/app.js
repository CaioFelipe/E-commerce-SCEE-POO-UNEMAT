let carrinho = [];
let token = localStorage.getItem('token');
let usuario = JSON.parse(localStorage.getItem('usuario'));
let produtosGlobais = [];
let valorFreteAtual = 0; // Variável global para guardar o frete gerado

document.addEventListener('DOMContentLoaded', () => {
    carregarCategorias(); // Carrega o select
    carregarProdutos(); 
    atualizarInterfaceAuth();
    atualizarContadorCarrinho();
    // NOVO: Ouve alterações no campo Bairro para calcular frete
    document.getElementById('end-bairro').addEventListener('blur', calcularFreteSimulado);
});

function calcularFreteSimulado() {
    const rua = document.getElementById('end-rua').value;
    const bairro = document.getElementById('end-bairro').value;

    // Só calcula se tiver endereço preenchido
    if (rua && bairro) {
        // Simula cálculo: Entre 15.00 e 30.00
        valorFreteAtual = (Math.random() * (30 - 15) + 15);
        
        // Atualiza a UI visualmente
        const subtotal = parseFloat(document.getElementById('cart-subtotal').innerText);
        atualizarTotaisUI(subtotal);
        
        // Feedback visual no campo de frete
        const elFrete = document.getElementById('cart-frete');
        elFrete.style.color = '#00ff00'; // Flash verde
        setTimeout(() => elFrete.style.color = 'var(--accent-color)', 500);
    }
}

// --- CATEGORIAS (NOVO) ---
async function carregarCategorias() {
    try {
        const categorias = await api.get('/web/categorias');
        const select = document.getElementById('filter-categoria');
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.innerText = cat.nome;
            select.appendChild(option);
        });
    } catch(e) {
        console.error("Erro categorias:", e);
    }
}

// --- PRODUTOS ---
async function carregarProdutos(filtros = {}) {
    const grid = document.getElementById('product-list');
    grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Carregando...</p>';

    const params = new URLSearchParams(filtros).toString();
    
    try {
        const produtos = await api.get(`/web/produtos?${params}`);
        produtosGlobais = produtos; // Salva para usar no modal de detalhes
        
        grid.innerHTML = ''; 

        if (produtos.length === 0) {
            grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center;">Nenhum produto encontrado.</p>';
            return;
        }

        produtos.forEach(p => {
            const card = document.createElement('div');
            card.className = 'product-card';
            
            const apiBase = "http://127.0.0.1:5000"; 
            const imgUrl = p.imagem_url ? `${apiBase}/uploads/${p.imagem_url}` : null;
            const imgTag = imgUrl 
                ? `<img src="${imgUrl}" alt="${p.nome}" onerror="this.src='https://placehold.co/150x150?text=Sem+Imagem'">`
                : `<img src="https://placehold.co/150x150?text=Sem+Imagem" alt="${p.nome}">`;

            // HTML Atualizado:
            // 1. Div clicável envolvendo imagem e título para abrir detalhes
            // 2. Removido o div de estoque
            card.innerHTML = `
                <div style="cursor: pointer;" onclick="abrirDetalhesProduto(${p.id})">
                    ${imgTag}
                    <h3>${p.nome}</h3>
                </div>
                
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
        grid.innerHTML = `<p style="color: var(--danger-color);">Erro: ${error.message}</p>`;
    }
}

// --- NOVO: LÓGICA DE DETALHES DO PRODUTO ---
function abrirDetalhesProduto(id) {
    const p = produtosGlobais.find(prod => prod.id === id);
    if (!p) return;

    // Preenche os dados
    document.getElementById('det-nome').innerText = p.nome;
    document.getElementById('det-sku').innerText = `SKU: ${p.sku}`;
    document.getElementById('det-desc').innerText = p.descricao || "Sem descrição disponível.";
    document.getElementById('det-preco').innerText = p.preco.toFixed(2);
    
    // Imagem
    const apiBase = "http://127.0.0.1:5000";
    document.getElementById('det-img').src = p.imagem_url 
        ? `${apiBase}/uploads/${p.imagem_url}` 
        : 'https://placehold.co/150x150?text=Sem+Imagem';

    // Configura o Botão de Adicionar (Estoque e Ação)
    const btn = document.getElementById('det-btn-add');
    const avisoEstoque = document.getElementById('det-estoque-aviso');

    if (p.estoque > 0) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-cart-plus"></i> Adicionar ao Carrinho';
        btn.onclick = () => {
            adicionarAoCarrinho(p.id, p.nome, p.preco);
            toggleDetalhesProduto(); // Fecha modal após adicionar
        };
        btn.style.backgroundColor = 'var(--accent-color)';
        btn.style.cursor = 'pointer';
        
        // Mostra "Últimas unidades" se estoque baixo (< 5)
        if(p.estoque < 5) {
            avisoEstoque.innerText = `Restam apenas ${p.estoque} un!`;
        } else {
            avisoEstoque.innerText = "Em estoque";
            avisoEstoque.style.color = "var(--success-color)";
        }
    } else {
        btn.disabled = true;
        btn.innerText = "Produto Indisponível";
        btn.style.backgroundColor = '#555';
        btn.style.cursor = 'not-allowed';
        avisoEstoque.innerText = "Esgotado";
        avisoEstoque.style.color = "var(--danger-color)";
    }

    const modal = document.getElementById('modal-produto');
    modal.classList.remove('hidden');
}

function toggleDetalhesProduto() {
    document.getElementById('modal-produto').classList.toggle('hidden');
}

function aplicarFiltros() {
    const min = document.getElementById('filter-min').value;
    const max = document.getElementById('filter-max').value;
    const busca = document.getElementById('filter-busca').value;
    const cat = document.getElementById('filter-categoria').value; // Novo
    
    const filtros = {};
    if (min) filtros.min_price = min;
    if (max) filtros.max_price = max;
    if (busca) filtros.busca = busca;
    if (cat) filtros.categoria_id = cat; // Novo
    
    carregarProdutos(filtros);
}

function limparFiltros() {
    document.getElementById('filter-min').value = '';
    document.getElementById('filter-max').value = '';
    document.getElementById('filter-busca').value = '';
    document.getElementById('filter-categoria').value = '';
    carregarProdutos();
}

// --- MEUS PEDIDOS (ATUALIZADO COM RASTREIO) ---
async function abrirMeusPedidos() {
    toggleProfile(); document.getElementById('modal-pedidos').classList.remove('hidden');
    const cont = document.getElementById('lista-pedidos-container'); cont.innerHTML = '<p>Carregando...</p>';
    try {
        const pedidos = await api.get('/web/meus-pedidos'); cont.innerHTML = '';
        if (pedidos.length === 0) { cont.innerHTML = '<p>Sem pedidos.</p>'; return; }
        pedidos.forEach(p => {
            let itensHtml = '';
            p.itens.forEach(i => {
                const img = i.imagem_url ? `http://127.0.0.1:5000/uploads/${i.imagem_url}` : 'https://placehold.co/150x150?text=Sem+Imagem';
                itensHtml += `<div style="display:flex;align-items:center;margin-top:10px;background:#252525;padding:5px;border-radius:4px;"><img src="${img}" style="width:40px;height:40px;object-fit:cover;margin-right:10px;"><div style="flex:1;">${i.nome}</div><div style="width:100px;text-align:right;">${i.quantidade}x R$ ${i.preco_unitario.toFixed(2)}</div></div>`;
                
            });
            
            
            // Lógica Rastreio e Cancelar
            let acoesHtml = '';
            if (p.status === 'Processando') {
                acoesHtml = `<button onclick="cancelarPedido(${p.id})" style="background:var(--danger-color);color:white;border:none;padding:5px;border-radius:4px;cursor:pointer;font-size:0.8rem;margin-top:5px;">Cancelar</button>`;
            } else if (p.status === 'Enviado' && p.codigo_rastreio) {
                acoesHtml = `<div style="margin-top:5px;padding:8px;background:#2a2a2a;border:1px dashed var(--accent-color);border-radius:4px;color:var(--accent-color);font-size:0.9rem;"><i class="fas fa-truck"></i> Rastreio: <strong>${p.codigo_rastreio}</strong></div>`;
            }
            
            const div = document.createElement('div');
            div.style = "background:#1e1e1e;padding:15px;border-radius:8px;margin-bottom:20px;border:1px solid #333;";
            div.innerHTML = `
                <div style="display:flex;justify-content:space-between;border-bottom:1px solid #444;padding-bottom:10px;margin-bottom:10px;">
                    <span style="color:var(--accent-color);font-weight:bold;">Pedido #${p.id}</span><span style="color:#aaa;">${p.data_pedido}</span>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <span>Status: <strong style="color:${getStatusColor(p.status)}">${p.status}</strong></span>
                        <br>${acoesHtml}
                    </div>
                    <span>Total: <strong style="font-size:1.2rem;">R$ ${p.total.toFixed(2)}</strong></span>
                </div>
                <div style="margin-top:10px;"><small style="color:#888;">Entregar em: ${p.endereco_entrega}</small></div>
                <div style="margin-top:15px;"><h5 style="margin:0 0 5px 0;">Itens:</h5>${itensHtml}</div>
            `;
            cont.appendChild(div);
        });
    } catch(e) { cont.innerHTML = `<p style="color:red;">Erro: ${e.message}</p>`; }
}
function getStatusColor(s) { if(s==='Enviado') return 'var(--success-color)'; if(s==='Cancelado') return 'var(--danger-color)'; return 'orange'; }
async function cancelarPedido(id) { if(!confirm("Cancelar?")) return; try{ await api.put(`/web/pedidos/${id}/cancelar`); document.getElementById('modal-pedidos').classList.add('hidden'); abrirMeusPedidos(); } catch(e){ alert(e.message); } }
function togglePedidos() { document.getElementById('modal-pedidos').classList.toggle('hidden'); }

// Helper para cores de status
function getStatusColor(status) {
    if (status === 'Enviado') return 'var(--success-color)';
    if (status === 'Cancelado') return 'var(--danger-color)';
    return 'orange'; // Processando
}

// Função chamada pelo botão
async function cancelarPedido(id) {
    if (!confirm("Tem certeza que deseja cancelar este pedido?")) return;

    try {
        const res = await api.put(`/web/pedidos/${id}/cancelar`);
        alert(res.mensagem);
        
        // Fecha e reabre o modal para atualizar a lista
        document.getElementById('modal-pedidos').classList.add('hidden');
        abrirMeusPedidos(); 
    } catch (e) {
        alert(`Erro ao cancelar: ${e.message}`);
    }
}

function togglePedidos() { document.getElementById('modal-pedidos').classList.toggle('hidden'); }

// CARRINHO, CHECKOUT E AUTH (Mantém igual ao anterior)
function adicionarAoCarrinho(id, nome, preco) {
    const item = carrinho.find(i => i.produto_id === id);
    if (item) item.qtd++; else carrinho.push({ produto_id: id, nome, preco_unitario: preco, qtd: 1 });
    atualizarContadorCarrinho();
    const btn = document.getElementById('btn-cart');
    btn.style.color = 'var(--success-color)'; setTimeout(() => btn.style.color = '', 500);
}
function atualizarContadorCarrinho() { 
    document.getElementById('cart-count').innerText = carrinho.reduce((acc, i) => acc + i.qtd, 0); 
}
function renderizarCarrinho() {
    const container = document.getElementById('cart-items'); 
    container.innerHTML = '';
    
    // Reseta frete visualmente se fechar e abrir
    valorFreteAtual = 0; 
    
    if (carrinho.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #777;">Vazio.</p>';
        document.getElementById('btn-checkout-start').style.display = 'none';
        document.getElementById('checkout-area').classList.add('hidden');
        atualizarTotaisUI(0);
    } else {
        document.getElementById('btn-checkout-start').style.display = 'block';
        let subtotal = 0;
        carrinho.forEach((item, idx) => {
            const sub = item.qtd * item.preco_unitario; 
            subtotal += sub;
            container.innerHTML += `<div class="cart-item"><span>${item.qtd}x ${item.nome}</span><div><span style="margin-right:10px;">R$ ${sub.toFixed(2)}</span><button onclick="removerDoCarrinho(${idx})" style="color:var(--danger-color); background:none; border:none; cursor:pointer;">&times;</button></div></div>`;
        });
        atualizarTotaisUI(subtotal);
    }
}
function atualizarTotaisUI(subtotal) {
    document.getElementById('cart-subtotal').innerText = subtotal.toFixed(2);
    document.getElementById('cart-frete').innerText = valorFreteAtual.toFixed(2);
    const totalFinal = subtotal + valorFreteAtual;
    document.getElementById('cart-total-final').innerText = totalFinal.toFixed(2);
}
function removerDoCarrinho(i) { 
    carrinho.splice(i, 1); 
    renderizarCarrinho(); 
    atualizarContadorCarrinho(); 
}
async function iniciarCheckout() {
    if (!token) { alert("Faça login."); toggleCart(); toggleLogin(); return; }
    
    document.getElementById('checkout-area').classList.remove('hidden');
    document.getElementById('btn-checkout-start').classList.add('hidden');
    
    // Tenta carregar endereço salvo
    try { 
        const p = await api.get('/web/perfil'); 
        if (p.endereco) { 
            document.getElementById('end-rua').value = p.endereco.rua || ''; 
            document.getElementById('end-num').value = p.endereco.numero || ''; 
            document.getElementById('end-bairro').value = p.endereco.bairro || ''; 
            
            // Se já tem endereço, calcula frete na hora!
            if(p.endereco.bairro) calcularFreteSimulado();
        } 
    } catch(e){}
}

function togglePagamento() { 
    const m = document.querySelector('input[name="pagamento"]:checked').value; 
    document.getElementById('div-cartao').classList.toggle('hidden', m !== 'cartao'); 
}
async function finalizarCompra() {
    const rua = document.getElementById('end-rua').value; 
    const num = document.getElementById('end-num').value; 
    const bairro = document.getElementById('end-bairro').value;
    
    if (!rua || !num || !bairro) { alert("Endereço obrigatório!"); return; }
    
    const metodo = document.querySelector('input[name="pagamento"]:checked').value; 
    const dadosPag = {};
    if (metodo === 'cartao') { 
        const card = document.getElementById('pag-cartao-num').value; 
        if (!card || card.length < 13) { alert("Cartão inválido."); return; } 
        dadosPag.numero_cartao = card; 
    }
    
    const totalFinal = parseFloat(document.getElementById('cart-total-final').innerText);
    
    const payload = { 
        itens: carrinho, 
        total: totalFinal, // Envia o total JÁ COM FRETE
        valor_frete: valorFreteAtual, // Envia o frete separado para registro
        endereco: { rua, numero: num, bairro }, 
        metodo_pagamento: metodo, 
        dados_pagamento: dadosPag 
    };
    
    const btn = document.querySelector('#checkout-area button'); 
    btn.innerText = "Processando..."; 
    btn.disabled = true;

    try { 
        const res = await api.post('/web/checkout', payload); 
        alert(`Pedido Confirmado!\nID: ${res.pedido_id}\nFrete: R$ ${valorFreteAtual.toFixed(2)}`); 
        carrinho = []; 
        toggleCart(); 
        atualizarContadorCarrinho(); 
        carregarProdutos(); 
    } catch (e) { 
        alert(`Erro: ${e.message}`); 
    } finally { 
        btn.innerText = "FINALIZAR PEDIDO"; 
        btn.disabled = false; 
    }
}
async function fazerLogin() {
    // Se o evento foi passado (ex: clique de botão ou enter), previne o refresh
    if (window.event) window.event.preventDefault();

    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-pass').value;
    const errorMsg = document.getElementById('login-error');
    
    errorMsg.innerText = '';

    if (!email || !senha) {
        errorMsg.innerText = 'Preencha todos os campos.';
        return;
    }

    const btn = document.querySelector('#modal-login button.btn-add');
    const textoOriginal = btn.innerText;
    btn.innerText = "Entrando...";
    btn.disabled = true;

    try {
        const data = await api.post('/gestao/login', { email, senha });

        token = data.token;
        usuario = data.usuario;
        
        // Salva sem stringify extra para o token
        localStorage.setItem('token', token);
        localStorage.setItem('usuario', JSON.stringify(usuario));

        toggleLogin();
        atualizarInterfaceAuth();
        
        // Limpa campos
        document.getElementById('login-email').value = '';
        document.getElementById('login-pass').value = '';
        
        // Feedback visual
        // alert(`Bem-vindo(a), ${usuario.nome}!`); // Opcional

    } catch (error) {
        // Agora o erro vai aparecer aqui em vez de recarregar a página!
        console.error("Erro no login:", error);
        errorMsg.innerText = error.message || 'Credenciais inválidas.';
    } finally {
        btn.innerText = textoOriginal;
        btn.disabled = false;
    }
}
async function fazerCadastro() {
    const nome = document.getElementById('cad-nome').value; const cpf = document.getElementById('cad-cpf').value; const email = document.getElementById('cad-email').value; const s1 = document.getElementById('cad-senha').value; const s2 = document.getElementById('cad-senha-conf').value;
    if (!nome || !cpf || !email || !s1) return; if (s1 !== s2) { document.getElementById('cad-error').innerText = 'Senhas diferem'; return; }
    try { await api.post('/web/cadastro', {nome, email, cpf, senha: s1}); alert("Criado! Login..."); toggleCadastro(); toggleLogin(); } catch(e) { document.getElementById('cad-error').innerText = e.message; }
}
async function carregarPerfil() { try { const p = await api.get('/web/perfil'); document.getElementById('perf-nome').value = p.nome; document.getElementById('perf-email').value = p.email; document.getElementById('perf-cpf').value = p.cpf || ''; } catch(e){} }
async function salvarPerfil() {
    const nome = document.getElementById('perf-nome').value; const email = document.getElementById('perf-email').value;
    try { await api.put('/web/perfil', {nome, email}); usuario.nome = nome; usuario.email = email; localStorage.setItem('usuario', JSON.stringify(usuario)); alert("Atualizado!"); toggleProfile(); atualizarInterfaceAuth(); } catch(e) { alert(e.message); }
}
function logout() { localStorage.clear(); window.location.reload(); }
function atualizarInterfaceAuth() {
    const disp = document.getElementById('user-display'); const log = document.getElementById('btn-login'); const prof = document.getElementById('btn-profile'); const out = document.getElementById('btn-logout');
    if (token && usuario) { disp.innerText = `Olá, ${usuario.nome.split(' ')[0]}`; disp.classList.remove('hidden'); log.classList.add('hidden'); prof.classList.remove('hidden'); out.classList.remove('hidden'); }
    else { disp.classList.add('hidden'); log.classList.remove('hidden'); prof.classList.add('hidden'); out.classList.add('hidden'); }
}
function toggleLogin() { document.getElementById('modal-login').classList.toggle('hidden'); }
function toggleCadastro() { document.getElementById('modal-cadastro').classList.toggle('hidden'); }
function toggleProfile() { const m = document.getElementById('modal-profile'); m.classList.toggle('hidden'); if(!m.classList.contains('hidden')) carregarPerfil(); }
function toggleCart() { const m = document.getElementById('modal-cart'); m.classList.toggle('hidden'); if(!m.classList.contains('hidden')) renderizarCarrinho(); }
function alternarParaCadastro() { toggleLogin(); toggleCadastro(); }
function alternarParaLogin() { toggleCadastro(); toggleLogin(); }
async function carregarProdutos(f={}){
    const g=document.getElementById('product-list');g.innerHTML='Loading...';
    const p=new URLSearchParams(f).toString();
    try{const r=await api.get(`/web/produtos?${p}`);
    produtosGlobais=r;g.innerHTML='';if(r.length===0){g.innerHTML='Nada.';return}r.forEach(x=>{const c=document.createElement('div');
        c.className='product-card';
        const im=x.imagem_url?`http://127.0.0.1:5000/uploads/${x.imagem_url}`:null;const tag=im?`<img src="${im}" onerror="https://placehold.co/150x150?text=Sem+Imagem'">`:`<img src="https://placehold.co/150x150?text=Sem+Imagem">`;
        c.innerHTML=`<div onclick="abrirDetalhesProduto(${x.id})" style="cursor:pointer">${tag}<h3>${x.nome}</h3></div><div class="price">R$ ${x.preco.toFixed(2)}</div><button class="btn-add" ${x.estoque>0?'':'disabled style="background:#555"'} onclick="adicionarAoCarrinho(${x.id},'${x.nome.replace(/'/g,"\\'")}',${x.preco})">${x.estoque>0?'Adicionar':'Indisponível'}</button>`;g.appendChild(c)})}catch(e){g.innerHTML=e.message}}

