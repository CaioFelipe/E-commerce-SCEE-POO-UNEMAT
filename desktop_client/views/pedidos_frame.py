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
        
        btn_enviar = tk.Button(toolbar, text="Marcar como Enviado", command=self.despachar_pedido, bg="#28a745", fg="white")
        btn_enviar.pack(side="left", padx=5)

        # Tabela de Pedidos (Treeview)
        # Mudamos a coluna 'cliente' para exibir Nome
        columns = ("id", "cliente", "total", "status", "endereco")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=50, anchor="center")
        
        self.tree.heading("cliente", text="Cliente") # Antes era "Cliente (ID)"
        self.tree.column("cliente", width=150, anchor="w")
        
        self.tree.heading("total", text="Total (R$)")
        self.tree.column("total", width=100, anchor="e")
        
        self.tree.heading("status", text="Status")
        self.tree.column("status", width=100, anchor="center")
        
        self.tree.heading("endereco", text="Endereço de Entrega")
        self.tree.column("endereco", width=350)

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
        pedidos = bridge.listar_pedidos() 

        # Se vier vazio ou None, não faz nada
        if not pedidos:
            return

        for p in pedidos:
            valor_fmt = f"R$ {p['total']:.2f}"
            
            # Tenta pegar o nome, se não vier (código antigo), usa ID ou "Desconhecido"
            cliente_display = p.get('cliente_nome', 'Cliente #' + str(p.get('cliente_id', '?')))
            
            # Estilização simples baseada no status
            status = p['status']
            
            item_id = self.tree.insert("", "end", values=(
                p['id'], 
                cliente_display, 
                valor_fmt, 
                status, 
                p['endereco_entrega']
            ))

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
            self.carregar_dados() 
        else:
            messagebox.showerror("Erro", "Falha ao atualizar status no servidor.")