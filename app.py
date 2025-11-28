from flask import Flask, render_template, request, redirect, url_for, session
from repositories import ProdutoRepositorio
from models import Carrinho

app = Flask(__name__)
app.secret_key = 'chave_secreta_scee' # Necessário para sessão

repo = ProdutoRepositorio()

# Simulação de carrinho na sessão (em produção seria persistido em banco)
def get_carrinho():
    if 'carrinho' not in session:
        session['carrinho'] = []
    return session['carrinho']

@app.route('/')
def index():
    produtos = repo.buscar_todos()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/<int:id>')
def detalhe_produto(id):
    produto = repo.buscar_por_id(id)
    return render_template('produto_detalhe.html', produto=produto)

@app.route('/adicionar/<int:id>')
def adicionar_ao_carrinho(id):
    # Lógica simplificada para demonstração
    carrinho = get_carrinho()
    carrinho.append(id)
    session['carrinho'] = carrinho
    return redirect(url_for('index'))

@app.route('/carrinho')
def ver_carrinho():
    ids = get_carrinho()
    itens = []
    total = 0
    # Agrupar itens e buscar objetos completos
    from collections import Counter
    contagem = Counter(ids)
    
    for id_prod, qtd in contagem.items():
        prod = repo.buscar_por_id(id_prod)
        if prod:
            itens.append({'produto': prod, 'quantidade': qtd, 'subtotal': prod.preco * qtd})
            total += prod.preco * qtd
            
    return render_template('carrinho.html', itens=itens, total=total)

if __name__ == '__main__':
    app.run(debug=True)
