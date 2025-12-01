import tkinter as tk
from tkinter import ttk
from .pedidos_frame import PedidosFrame
from .produtos_frame import ProdutosFrame

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Header
        header = tk.Frame(self, bg="#333", height=50)
        header.pack(side="top", fill="x")
        
        self.lbl_user = tk.Label(header, text="Bem-vindo, Admin", bg="#333", fg="white", font=("Arial", 12))
        self.lbl_user.pack(side="left", padx=20, pady=10)

        btn_logout = tk.Button(header, text="Sair", bg="#d9534f", fg="white", bd=0, command=self.logout)
        btn_logout.pack(side="right", padx=20, pady=10)

        # Sistema de Abas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Instancia as abas
        self.pedidos_tab = PedidosFrame(self.notebook, controller)
        self.produtos_tab = ProdutosFrame(self.notebook, controller)

        self.notebook.add(self.pedidos_tab, text=" Gerenciar Pedidos ")
        self.notebook.add(self.produtos_tab, text=" Cadastrar Produto ")
        
        # Evento para carregar dados ao trocar de aba ou mostrar a tela
        self.bind("<<Show>>", self.on_show)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_show(self, event):
        """Chamado quando esta View vem para o topo."""
        bridge = self.controller.get_bridge()
        if bridge.usuario_atual:
            self.lbl_user.config(text=f"Logado como: {bridge.usuario_atual.get('nome', 'Admin')}")
        
        # Carrega dados iniciais da aba de pedidos
        self.pedidos_tab.carregar_dados()

    def on_tab_change(self, event):
        # Se mudou para a aba de pedidos, recarrega a lista
        if self.notebook.select() == self.notebook.tabs()[0]:
            self.pedidos_tab.carregar_dados()

    def logout(self):
        bridge = self.controller.get_bridge()
        bridge.token = None
        bridge.usuario_atual = None
        self.controller.show_frame("LoginView")