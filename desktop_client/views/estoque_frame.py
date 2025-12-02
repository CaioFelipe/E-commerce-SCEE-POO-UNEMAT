import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class EstoqueFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.produtos_cache = []
        self.lista_categorias = []
        
        # Estado
        self.produto_selecionado_id = None
        self.imagem_atual_nome = ""
        self.nova_imagem_local = None
        self.remover_imagem = False

        # Layout
        paned = tk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)
        
        # --- LADO ESQUERDO ---
        frame_lista = tk.Frame(paned, padx=5, pady=5)
        paned.add(frame_lista, width=450)
        
        # Filtros
        frm_filtro = tk.LabelFrame(frame_lista, text="Filtros de Pesquisa", padx=5, pady=5)
        frm_filtro.pack(fill="x")
        
        tk.Label(frm_filtro, text="Nome ou SKU:").pack(anchor="w")
        self.entry_busca = tk.Entry(frm_filtro)
        self.entry_busca.pack(fill="x", pady=(0, 5))
        
        frame_cat_btn = tk.Frame(frm_filtro)
        frame_cat_btn.pack(fill="x")
        tk.Label(frame_cat_btn, text="Categoria:").pack(side="left")
        self.combo_filtro_cat = ttk.Combobox(frame_cat_btn, state="readonly", width=20)
        self.combo_filtro_cat.pack(side="left", padx=5)
        
        tk.Button(frame_cat_btn, text="🔍 Buscar", command=self.carregar_dados, bg="#e0e0e0").pack(side="right")
        
        # Tabela
        cols = ("id", "sku", "nome", "cat", "estoque", "preco")
        self.tree = ttk.Treeview(frame_lista, columns=cols, show="headings")
        self.tree.heading("id", text="ID"); self.tree.column("id", width=30)
        self.tree.heading("sku", text="SKU"); self.tree.column("sku", width=70)
        self.tree.heading("nome", text="Nome"); self.tree.column("nome", width=120)
        self.tree.heading("cat", text="Categoria"); self.tree.column("cat", width=80)
        self.tree.heading("estoque", text="Qtd"); self.tree.column("estoque", width=40)
        self.tree.heading("preco", text="Preço"); self.tree.column("preco", width=60)
        
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.preencher_formulario)

        # --- LADO DIREITO ---
        frame_form = tk.LabelFrame(paned, text="Editar Detalhes", padx=10, pady=10)
        paned.add(frame_form)
        
        self.campos = {}
        
        tk.Label(frame_form, text="ID:", font=("Arial", 8)).pack(anchor="w")
        self.lbl_id = tk.Label(frame_form, text="-", font=("Arial", 10, "bold"), fg="blue")
        self.lbl_id.pack(anchor="w", pady=(0, 5))

        # Campos
        for label, key in [("Nome", "nome"), ("SKU", "sku"), ("Preço (R$)", "preco"), ("Estoque", "estoque")]:
            tk.Label(frame_form, text=label).pack(anchor="w")
            entry = tk.Entry(frame_form)
            entry.pack(fill="x", pady=(0, 2))
            self.campos[key] = entry

        tk.Label(frame_form, text="Categoria").pack(anchor="w")
        self.combo_edit_cat = ttk.Combobox(frame_form, state="readonly")
        self.combo_edit_cat.pack(fill="x", pady=(0, 2))

        tk.Label(frame_form, text="Descrição").pack(anchor="w")
        self.txt_descricao = tk.Text(frame_form, height=4, width=30)
        self.txt_descricao.pack(fill="x", pady=(0, 5))

        # Imagem
        tk.Label(frame_form, text="Imagem", font=("Arial", 9, "bold")).pack(anchor="w")
        self.lbl_img_atual = tk.Label(frame_form, text="Sem imagem", fg="#777")
        self.lbl_img_atual.pack(anchor="w")
        
        frm_img = tk.Frame(frame_form)
        frm_img.pack(fill="x")
        tk.Button(frm_img, text="Alterar...", command=self.selecionar_nova_imagem).pack(side="left")
        tk.Button(frm_img, text="Remover", command=self.remover_imagem_acao, fg="red").pack(side="left", padx=5)

        tk.Button(frame_form, text="SALVAR", bg="#007bff", fg="white", font=("Arial", 10, "bold"), command=self.salvar_edicao).pack(fill="x", pady=15, side="bottom")

        # Não chamamos carregar_dados() aqui no __init__, pois o login ainda não ocorreu.
        # Será chamado pelo DashboardView.

    def carregar_categorias(self):
        bridge = self.controller.get_bridge()
        cats = bridge.listar_categorias()
        self.lista_categorias = cats
        
        nomes = ["Todas"] + [c['nome'] for c in cats]
        
        # Salva a seleção atual para não perder ao recarregar
        sel_filtro = self.combo_filtro_cat.get()
        self.combo_filtro_cat['values'] = nomes
        if not sel_filtro: self.combo_filtro_cat.current(0)
        
        self.combo_edit_cat['values'] = [c['nome'] for c in cats]

    def carregar_dados(self):
        # 1. ATUALIZAÇÃO CRÍTICA: Carrega categorias com Token válido
        self.carregar_categorias()
        
        # Limpa tabela
        for i in self.tree.get_children(): self.tree.delete(i)
        
        # Filtros
        filtros = {}
        termo = self.entry_busca.get()
        if termo: filtros['termo'] = termo
        
        cat_sel = self.combo_filtro_cat.get()
        if cat_sel and cat_sel != "Todas":
            cat_id = next((c['id'] for c in self.lista_categorias if c['nome'] == cat_sel), None)
            if cat_id: filtros['categoria_id'] = cat_id

        # Busca
        bridge = self.controller.get_bridge()
        produtos = bridge.listar_produtos(filtros)
        self.produtos_cache = produtos
        
        for p in produtos:
            cat_nome = p.get('categoria_nome', '-')
            self.tree.insert("", "end", values=(p['id'], p['sku'], p['nome'], cat_nome, p['estoque'], f"R$ {p['preco']:.2f}"))

    def preencher_formulario(self, event):
        sel = self.tree.selection()
        if not sel: return
        p_id = int(self.tree.item(sel[0], 'values')[0])
        prod = next((p for p in self.produtos_cache if p['id'] == p_id), None)
        if not prod: return
        
        self.produto_selecionado_id = p_id
        self.nova_imagem_local = None
        self.remover_imagem = False
        self.imagem_atual_nome = prod.get('imagem_url', '')
        
        self.lbl_id.config(text=f"#{p_id}")
        self.lbl_img_atual.config(text=self.imagem_atual_nome if self.imagem_atual_nome else "Sem imagem", fg="black")
        
        self.campos['nome'].delete(0, tk.END); self.campos['nome'].insert(0, prod['nome'])
        self.campos['sku'].delete(0, tk.END); self.campos['sku'].insert(0, prod['sku'])
        self.campos['preco'].delete(0, tk.END); self.campos['preco'].insert(0, prod['preco'])
        self.campos['estoque'].delete(0, tk.END); self.campos['estoque'].insert(0, prod['estoque'])
        
        self.txt_descricao.delete("1.0", tk.END)
        self.txt_descricao.insert("1.0", prod.get('descricao', ''))
        
        if prod.get('categoria_id'):
            c_nome = next((c['nome'] for c in self.lista_categorias if c['id'] == prod['categoria_id']), '')
            self.combo_edit_cat.set(c_nome)
        else: self.combo_edit_cat.set('')

    def selecionar_nova_imagem(self):
        f = filedialog.askopenfilename(filetypes=(("Imagens", "*.jpg;*.png"),))
        if f:
            self.nova_imagem_local = f
            self.remover_imagem = False
            self.lbl_img_atual.config(text=f"Nova: {os.path.basename(f)}", fg="blue")

    def remover_imagem_acao(self):
        self.remover_imagem = True
        self.nova_imagem_local = None
        self.lbl_img_atual.config(text="Será removida", fg="red")

    def salvar_edicao(self):
        if not self.produto_selecionado_id: return
        bridge = self.controller.get_bridge()
        
        img_final = self.imagem_atual_nome
        if self.remover_imagem: img_final = ""
        elif self.nova_imagem_local:
            ok, res = bridge.enviar_imagem(self.nova_imagem_local)
            if ok: img_final = res
            else: 
                messagebox.showerror("Erro", res)
                return

        try:
            dados = {
                'nome': self.campos['nome'].get(),
                'sku': self.campos['sku'].get(),
                'preco': float(self.campos['preco'].get()),
                'estoque': int(self.campos['estoque'].get()),
                'descricao': self.txt_descricao.get("1.0", tk.END).strip(),
                'imagem_url': img_final
            }
            c_nome = self.combo_edit_cat.get()
            cid = next((c['id'] for c in self.lista_categorias if c['nome'] == c_nome), None)
            if cid: dados['categoria_id'] = cid
            
            ok, msg = bridge.atualizar_produto(self.produto_selecionado_id, dados)
            if ok: 
                messagebox.showinfo("Sucesso", "Atualizado!"); self.carregar_dados()
                self.lbl_id.config(text="-"); self.produto_selecionado_id = None
            else: messagebox.showerror("Erro", msg)
        except ValueError: messagebox.showerror("Erro", "Números inválidos")