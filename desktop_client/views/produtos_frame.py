import tkinter as tk
from tkinter import messagebox, filedialog
import os

class ProdutosFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Variável para guardar o caminho local da imagem selecionada
        self.caminho_imagem_local = None
        
        # Container Principal com Padding
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Título da Seção
        tk.Label(container, text="Novo Produto", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Dicionário para guardar as referências dos campos de input
        self.campos = {}
        
        # --- CRIAÇÃO DOS CAMPOS DO FORMULÁRIO ---
        
        # 1. Nome do Produto
        tk.Label(container, text="Nome:", anchor="w").grid(row=1, column=0, sticky="w")
        self.campos['nome'] = tk.Entry(container, width=40)
        self.campos['nome'].grid(row=1, column=1, sticky="w", pady=5)

        # 2. SKU (Código Único)
        tk.Label(container, text="SKU:", anchor="w").grid(row=2, column=0, sticky="w")
        self.campos['sku'] = tk.Entry(container, width=20)
        self.campos['sku'].grid(row=2, column=1, sticky="w", pady=5)

        # 3. Preço
        tk.Label(container, text="Preço (R$):", anchor="w").grid(row=3, column=0, sticky="w")
        self.campos['preco'] = tk.Entry(container, width=20)
        self.campos['preco'].grid(row=3, column=1, sticky="w", pady=5)

        # 4. Estoque Inicial
        tk.Label(container, text="Estoque:", anchor="w").grid(row=4, column=0, sticky="w")
        self.campos['estoque'] = tk.Entry(container, width=20)
        self.campos['estoque'].grid(row=4, column=1, sticky="w", pady=5)

        # 5. Imagem (Botão de Seleção de Arquivo)
        tk.Label(container, text="Imagem:", anchor="w").grid(row=5, column=0, sticky="w")
        
        # Frame auxiliar para agrupar botão e label de status
        frame_img = tk.Frame(container)
        frame_img.grid(row=5, column=1, sticky="w", pady=5)
        
        self.btn_img = tk.Button(frame_img, text="Selecionar Arquivo...", command=self.selecionar_imagem)
        self.btn_img.pack(side="left")
        
        # Label que mostrará o nome do arquivo selecionado ou status do upload
        self.lbl_img_status = tk.Label(frame_img, text="Nenhum arquivo selecionado", fg="#777", padx=10)
        self.lbl_img_status.pack(side="left")

        # 6. Descrição Detalhada
        tk.Label(container, text="Descrição:", anchor="w").grid(row=6, column=0, sticky="w")
        self.campos['descricao'] = tk.Entry(container, width=40)
        self.campos['descricao'].grid(row=6, column=1, sticky="w", pady=5)

        # Botão Principal de Ação
        btn_salvar = tk.Button(container, text="CADASTRAR PRODUTO", bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               command=self.salvar_produto)
        btn_salvar.grid(row=8, column=1, sticky="e", pady=20)

    def selecionar_imagem(self):
        """
        Abre a janela nativa do sistema operacional para escolher uma imagem.
        """
        filename = filedialog.askopenfilename(
            title="Selecione a imagem do produto",
            filetypes=(("Imagens", "*.jpg *.jpeg *.png"), ("Todos", "*.*"))
        )
        if filename:
            self.caminho_imagem_local = filename
            # Extrai apenas o nome do arquivo (ex: 'mouse.jpg') para exibir na tela
            nome_arquivo = os.path.basename(filename)
            self.lbl_img_status.config(text=nome_arquivo, fg="green")

    def salvar_produto(self):
        """
        Orquestra o processo de cadastro:
        1. Valida campos básicos.
        2. Faz upload da imagem (se houver).
        3. Envia os dados do produto para a API.
        """
        # Coleta os dados dos campos de texto (exceto imagem que é tratada à parte)
        dados = {k: v.get() for k, v in self.campos.items() if k != 'imagem_url'}

        # Validação Básica Frontend
        if not dados['nome'] or not dados['sku'] or not dados['preco']:
            messagebox.showwarning("Campos Obrigatórios", "Por favor, preencha Nome, SKU e Preço.")
            return

        bridge = self.controller.get_bridge()
        
        # --- PASSO 1: Upload da Imagem (se houver seleção local) ---
        nome_imagem_remota = ""
        if self.caminho_imagem_local:
            self.lbl_img_status.config(text="Enviando imagem...", fg="blue")
            self.update_idletasks() # Força a interface a atualizar o texto antes de travar no upload
            
            sucesso_upload, resultado = bridge.enviar_imagem(self.caminho_imagem_local)
            
            if sucesso_upload:
                nome_imagem_remota = resultado # O servidor retorna o nome salvo (ex: '17823_mouse.jpg')
                self.lbl_img_status.config(text="Upload OK!", fg="green")
            else:
                messagebox.showerror("Erro Upload", f"Falha ao enviar imagem: {resultado}")
                self.lbl_img_status.config(text="Erro no Upload", fg="red")
                return # Interrompe o processo se o upload falhar
        
        # --- PASSO 2: Cadastro do Produto ---
        dados['imagem_url'] = nome_imagem_remota
        
        try:
            # Garante tipos corretos para o JSON
            dados['preco'] = float(dados['preco'])
            dados['estoque'] = int(dados['estoque'])
        except ValueError:
            messagebox.showerror("Erro de Formato", "Preço e Estoque devem ser números válidos.")
            return

        # Envia para a API de Gestão
        sucesso = bridge.criar_produto(dados)

        if sucesso:
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            # Limpa o formulário para o próximo cadastro
            for entry in self.campos.values():
                entry.delete(0, tk.END)
            self.caminho_imagem_local = None
            self.lbl_img_status.config(text="Nenhum arquivo selecionado", fg="#777")
        else:
            messagebox.showerror("Erro", "Falha ao cadastrar produto. Verifique se o SKU já existe.")