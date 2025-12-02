import tkinter as tk
from tkinter import ttk
from .pedidos_frame import PedidosFrame
from .produtos_frame import ProdutosFrame
from .clientes_frame import ClientesFrame
from .estoque_frame import EstoqueFrame

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header
        header = tk.Frame(self, bg="#333", height=50)
        header.pack(side="top", fill="x")
        self.lbl_user = tk.Label(header, text="Admin", bg="#333", fg="white", font=("Arial", 12))
        self.lbl_user.pack(side="left", padx=20, pady=10)
        tk.Button(header, text="Sair", bg="#d9534f", fg="white", bd=0, command=self.logout).pack(side="right", padx=20, pady=10)

        # Abas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.pedidos_tab = PedidosFrame(self.notebook, controller)
        self.estoque_tab = EstoqueFrame(self.notebook, controller)
        self.produtos_tab = ProdutosFrame(self.notebook, controller)
        self.clientes_tab = ClientesFrame(self.notebook, controller)

        self.notebook.add(self.pedidos_tab, text=" 📦 Pedidos ")
        self.notebook.add(self.estoque_tab, text=" 📊 Estoque (Editar) ")
        self.notebook.add(self.produtos_tab, text=" ➕ Novo Produto ")
        self.notebook.add(self.clientes_tab, text=" 👥 Clientes ")
        
        self.bind("<<Show>>", self.on_show)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_show(self, event):
        bridge = self.controller.get_bridge()
        if bridge.usuario_atual:
            self.lbl_user.config(text=f"Logado como: {bridge.usuario_atual.get('nome', 'Admin')}")
        
        # Força atualização da aba atual ao fazer login
        self.atualizar_aba_atual()

    def on_tab_change(self, event):
        self.atualizar_aba_atual()

    def atualizar_aba_atual(self):
        # Descobre qual aba está visível e manda recarregar
        if self.notebook.select():
            index = self.notebook.index(self.notebook.select())
            if index == 0: self.pedidos_tab.carregar_dados()
            elif index == 1: self.estoque_tab.carregar_dados() # Aqui carrega categorias tb!
            elif index == 2: self.produtos_tab.carregar_categorias()
            elif index == 3: self.clientes_tab.carregar_dados()

    def logout(self):
        self.controller.get_bridge().token = None
        self.controller.show_frame("LoginView")