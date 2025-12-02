import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os

class ProdutosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.caminho_imagem_local = None
        self.lista_categorias = [] # Cache de categorias
        
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Novo Produto", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        self.campos = {}
        
        # Campos
        campos_texto = [("Nome:", "nome"), ("SKU:", "sku"), ("Preço (R$):", "preco"), ("Estoque:", "estoque")]
        row_idx = 1
        for label, key in campos_texto:
            tk.Label(container, text=label, anchor="w").grid(row=row_idx, column=0, sticky="w")
            entry = tk.Entry(container, width=30)
            entry.grid(row=row_idx, column=1, sticky="w", pady=5)
            self.campos[key] = entry
            row_idx += 1

        # Categoria (Combobox)
        tk.Label(container, text="Categoria:", anchor="w").grid(row=row_idx, column=0, sticky="w")
        self.combo_categoria = ttk.Combobox(container, width=27, state="readonly")
        self.combo_categoria.grid(row=row_idx, column=1, sticky="w", pady=5)
        row_idx += 1

        # Descrição
        tk.Label(container, text="Descrição:", anchor="w").grid(row=row_idx, column=0, sticky="w")
        self.campos['descricao'] = tk.Entry(container, width=30)
        self.campos['descricao'].grid(row=row_idx, column=1, sticky="w", pady=5)
        row_idx += 1

        # Imagem
        tk.Label(container, text="Imagem:", anchor="w").grid(row=row_idx, column=0, sticky="w")
        frame_img = tk.Frame(container)
        frame_img.grid(row=row_idx, column=1, sticky="w", pady=5)
        tk.Button(frame_img, text="Arquivo...", command=self.selecionar_imagem).pack(side="left")
        self.lbl_img_status = tk.Label(frame_img, text="Nenhum", fg="#777", padx=5)
        self.lbl_img_status.pack(side="left")
        row_idx += 1

        tk.Button(container, text="CADASTRAR", bg="#007bff", fg="white", command=self.salvar_produto).grid(row=row_idx, column=1, sticky="e", pady=20)

        # Carregar categorias ao iniciar
        self.carregar_categorias()

    def carregar_categorias(self):
        bridge = self.controller.get_bridge()
        cats = bridge.listar_categorias()
        self.lista_categorias = cats
        # Preenche o combobox com os nomes
        self.combo_categoria['values'] = [c['nome'] for c in cats]

    def selecionar_imagem(self):
        filename = filedialog.askopenfilename(filetypes=(("Imagens", "*.jpg *.jpeg *.png"),))
        if filename:
            self.caminho_imagem_local = filename
            self.lbl_img_status.config(text=os.path.basename(filename), fg="green")

    def salvar_produto(self):
        dados = {k: v.get() for k, v in self.campos.items()}
        
        # Pega ID da categoria selecionada
        nome_cat = self.combo_categoria.get()
        cat_id = next((c['id'] for c in self.lista_categorias if c['nome'] == nome_cat), None)
        
        if not cat_id:
            messagebox.showwarning("Aviso", "Selecione uma categoria válida.")
            return
        
        dados['categoria_id'] = cat_id

        # Validação e Upload (Igual anterior)
        if not dados['nome'] or not dados['sku'] or not dados['preco']:
            messagebox.showwarning("Aviso", "Campos obrigatórios vazios.")
            return

        bridge = self.controller.get_bridge()
        
        # Upload
        if self.caminho_imagem_local:
            ok, res = bridge.enviar_imagem(self.caminho_imagem_local)
            if ok: dados['imagem_url'] = res
            else: 
                messagebox.showerror("Erro Upload", res)
                return

        # Salvar
        try:
            dados['preco'] = float(dados['preco'])
            dados['estoque'] = int(dados['estoque'])
            if bridge.criar_produto(dados):
                messagebox.showinfo("Sucesso", "Produto criado!")
                for entry in self.campos.values(): entry.delete(0, tk.END)
                self.combo_categoria.set('')
                self.lbl_img_status.config(text="Nenhum")
                self.caminho_imagem_local = None
            else:
                messagebox.showerror("Erro", "Falha ao criar.")
        except ValueError: messagebox.showerror("Erro", "Valores numéricos inválidos.")