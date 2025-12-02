import tkinter as tk
from tkinter import ttk, messagebox, Toplevel

class PedidosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Barra de Topo
        toolbar = tk.Frame(self, bg="#e0e0e0", pady=5, padx=5)
        toolbar.pack(side="top", fill="x")
        tk.Button(toolbar, text="🔄 Atualizar Lista", command=self.carregar_dados).pack(side="left", padx=5)
        tk.Label(toolbar, text="Dê duplo clique no pedido para ver detalhes", bg="#e0e0e0", fg="#555").pack(side="right", padx=10)

        # Configuração de Estilo
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        # Tabela Principal
        columns = ("id", "cliente", "total", "status", "data")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("id", text="ID"); self.tree.column("id", width=50, anchor="center")
        self.tree.heading("cliente", text="Cliente"); self.tree.column("cliente", width=200)
        self.tree.heading("total", text="Total"); self.tree.column("total", width=100, anchor="e")
        self.tree.heading("status", text="Status"); self.tree.column("status", width=120, anchor="center")
        self.tree.heading("data", text="Data"); self.tree.column("data", width=150, anchor="center")

        self.tree.tag_configure('impar', background='#f9f9f9')
        self.tree.tag_configure('par', background='#e1e1e1')
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self.abrir_detalhes)

    def carregar_dados(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        
        bridge = self.controller.get_bridge()
        pedidos = bridge.listar_pedidos() 

        if not pedidos: return

        for i, p in enumerate(pedidos):
            tag = 'par' if i % 2 == 0 else 'impar'
            self.tree.insert("", "end", values=(
                p['id'], 
                p.get('cliente_nome', 'Desc.'), 
                f"R$ {p['total']:.2f}", 
                p['status'], 
                p['data_pedido']
            ), tags=(tag,))

    def abrir_detalhes(self, event):
        item_sel = self.tree.selection()
        if not item_sel: return
        
        # Pega ID da linha clicada
        valores_linha = self.tree.item(item_sel[0], 'values')
        pedido_id_lista = int(valores_linha[0])
        
        # --- BUSCA DETALHADA NA API ---
        bridge = self.controller.get_bridge()
        pedido = bridge.obter_pedido(pedido_id_lista)
        
        if not pedido:
            messagebox.showerror("Erro", "Não foi possível carregar os detalhes do pedido.")
            return

        # --- MODAL ---
        modal = Toplevel(self)
        modal.title(f"Detalhes do Pedido #{pedido['id']}")
        modal.geometry("700x600")
        
        # Container Principal
        main_frame = tk.Frame(modal, padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Cabeçalho (Cliente e Status)
        frame_head = tk.Frame(main_frame)
        # CORREÇÃO AQUI: Substituído marginBottom=20 por pady=(0, 20)
        frame_head.pack(fill="x", pady=(0, 20))
        
        tk.Label(frame_head, text=f"Pedido #{pedido['id']}", font=("Arial", 16, "bold")).pack(side="left")
        
        cor_status = "green" if pedido['status'] == "Enviado" else "orange"
        lbl_status = tk.Label(frame_head, text=pedido['status'], fg=cor_status, font=("Arial", 12, "bold"), bd=1, relief="solid", padx=10, pady=5)
        lbl_status.pack(side="right")

        # Info Cliente
        info_frame = tk.LabelFrame(main_frame, text="Dados do Cliente e Entrega", padx=10, pady=10)
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text=f"Cliente: {pedido.get('cliente_nome')} ({pedido.get('cliente_email')})", anchor="w", font=("Arial", 11, "bold")).pack(fill="x")
        tk.Label(info_frame, text=f"Data: {pedido['data_pedido']}", anchor="w").pack(fill="x")
        tk.Label(info_frame, text=f"Endereço: {pedido['endereco_entrega']}", anchor="w", font=("Arial", 10, "italic")).pack(fill="x", pady=5)
        
        if pedido.get('codigo_rastreio'):
            tk.Label(info_frame, text=f"Rastreio: {pedido['codigo_rastreio']}", fg="blue", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)

        # Tabela de Itens (O QUE FALTAVA)
        tk.Label(main_frame, text="Itens do Pedido:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
        
        frame_itens = tk.Frame(main_frame)
        frame_itens.pack(fill="both", expand=True)
        
        cols_itens = ("produto", "qtd", "unit", "sub")
        tree_itens = ttk.Treeview(frame_itens, columns=cols_itens, show="headings", height=6)
        tree_itens.heading("produto", text="Produto"); tree_itens.column("produto", width=250)
        tree_itens.heading("qtd", text="Qtd"); tree_itens.column("qtd", width=50, anchor="center")
        tree_itens.heading("unit", text="Unitário"); tree_itens.column("unit", width=80, anchor="e")
        tree_itens.heading("sub", text="Subtotal"); tree_itens.column("sub", width=80, anchor="e")
        tree_itens.pack(side="left", fill="both", expand=True)
        
        scroll_itens = ttk.Scrollbar(frame_itens, orient="vertical", command=tree_itens.yview)
        tree_itens.configure(yscroll=scroll_itens.set)
        scroll_itens.pack(side="right", fill="y")

        # Popula Itens
        for item in pedido.get('itens', []):
            subtotal = item['quantidade'] * item['preco_unitario']
            tree_itens.insert("", "end", values=(
                item['nome'],
                item['quantidade'],
                f"R$ {item['preco_unitario']:.2f}",
                f"R$ {subtotal:.2f}"
            ))

        # Totais
        frame_totais = tk.Frame(main_frame, pady=10)
        frame_totais.pack(fill="x")
        
        frete = pedido.get('valor_frete', 0)
        # Se frete for None por algum motivo no banco antigo, usa 0
        if frete is None: frete = 0
        
        total = pedido['total']
        subtotal_geral = total - frete
        
        tk.Label(frame_totais, text=f"Subtotal: R$ {subtotal_geral:.2f}").pack(anchor="e")
        tk.Label(frame_totais, text=f"Frete: R$ {frete:.2f}").pack(anchor="e")
        tk.Label(frame_totais, text=f"TOTAL FINAL: R$ {total:.2f}", font=("Arial", 14, "bold"), fg="green").pack(anchor="e")

        # Botão de Ação (Se aplicável)
        if pedido['status'] == "Processando":
            def despachar():
                if messagebox.askyesno("Confirmar", "Gerar código de rastreio e marcar como Enviado?"):
                    bridge = self.controller.get_bridge()
                    if bridge.atualizar_status_pedido(pedido['id'], "Enviado"):
                        messagebox.showinfo("Sucesso", "Pedido despachado!")
                        modal.destroy()
                        self.carregar_dados() # Recarrega lista principal
                    else:
                        messagebox.showerror("Erro", "Falha na comunicação")
                    
            tk.Button(main_frame, text="DESPACHAR PEDIDO", bg="#28a745", fg="white", font=("Arial", 10, "bold"), command=despachar).pack(fill="x", pady=10)