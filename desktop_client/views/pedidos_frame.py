import tkinter as tk
from tkinter import ttk, messagebox

class PedidosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Barra de Ferramentas
        toolbar = tk.Frame(self, bg="#e0e0e0", pady=5, padx=5)
        toolbar.pack(side="top", fill="x")

        tk.Button(toolbar, text="Atualizar Lista", command=self.carregar_dados).pack(side="left", padx=5)
        tk.Button(toolbar, text="Marcar como Enviado", command=self.despachar_pedido, bg="#28a745", fg="white").pack(side="left", padx=5)

        # Tabela de Pedidos (Treeview)
        columns = ("id", "cliente", "total", "status", "endereco")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        
        self.tree.heading("cliente", text="Cliente (ID)")
        self.tree.column("cliente", width=100, anchor="center")
        
        self.tree.heading("total", text="Total (R$)")
        self.tree.column("total", width=100, anchor="e")
        
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=120, anchor="center")
        
        self.tree.heading("endereco", text="Endereço de Entrega")
        self.tree.column("endereco", width=300)

        # Barra de Rolagem
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

    def carregar_dados(self):
        # Limpa tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        bridge = self.controller.get_bridge()
        pedidos = bridge.listar_pedidos() # Requisição GET para API

        for p in pedidos:
            # Formata valores para exibição
            valor_fmt = f"R$ {p['total']:.2f}"
            self.tree.insert("", "end", values=(p['id'], p['cliente_id'], valor_fmt, p['status'], p['endereco_entrega']))

    def despachar_pedido(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um pedido para despachar.")
            return

        item_data = self.tree.item(selected_item[0])
        pedido_id = item_data['values'][0]
        status_atual = item_data['values'][3]

        if status_atual == "Enviado":
            messagebox.showinfo("Info", "Este pedido já foi enviado.")
            return

        bridge = self.controller.get_bridge()
        sucesso = bridge.atualizar_status_pedido(pedido_id, "Enviado")

        if sucesso:
            messagebox.showinfo("Sucesso", f"Pedido #{pedido_id} marcado como ENVIADO!")
            self.carregar_dados() # Recarrega para mostrar novo status
        else:
            messagebox.showerror("Erro", "Falha ao atualizar status no servidor.")