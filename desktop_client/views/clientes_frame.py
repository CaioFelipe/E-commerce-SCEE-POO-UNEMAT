import tkinter as tk
from tkinter import ttk, Toplevel

class ClientesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Topo
        top = tk.Frame(self, bg="#e0e0e0", pady=5)
        top.pack(fill="x")
        tk.Button(top, text="🔄 Atualizar Clientes", command=self.carregar_dados).pack(side="left", padx=10)

        # Tabela
        self.tree = ttk.Treeview(self, columns=("id", "nome", "email", "cpf"), show="headings")
        self.tree.heading("id", text="ID"); self.tree.column("id", width=50)
        self.tree.heading("nome", text="Nome"); self.tree.column("nome", width=200)
        self.tree.heading("email", text="E-mail"); self.tree.column("email", width=200)
        self.tree.heading("cpf", text="CPF"); self.tree.column("cpf", width=100)
        
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.ver_historico)

    def carregar_dados(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        bridge = self.controller.get_bridge()
        clientes = bridge.listar_clientes()
        for c in clientes:
            self.tree.insert("", "end", values=(c['id'], c['nome_completo'], c['email'], c.get('cpf', '-')))

    def ver_historico(self, event):
        sel = self.tree.selection()
        if not sel: return
        
        item = self.tree.item(sel[0], 'values')
        cli_id, cli_nome = item[0], item[1]
        
        # Modal
        modal = Toplevel(self)
        modal.title(f"Histórico de: {cli_nome}")
        modal.geometry("500x400")
        
        tk.Label(modal, text=f"Pedidos de {cli_nome}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Lista simples de pedidos
        lista = tk.Listbox(modal, width=60, height=15)
        lista.pack(padx=10, pady=5)
        
        bridge = self.controller.get_bridge()
        pedidos = bridge.listar_pedidos_cliente(cli_id)
        
        if not pedidos:
            lista.insert("end", "Nenhum pedido encontrado.")
        else:
            for p in pedidos:
                lista.insert("end", f"#{p['id']} - {p['data_pedido']} - R$ {p['total']:.2f} - {p['status']}")