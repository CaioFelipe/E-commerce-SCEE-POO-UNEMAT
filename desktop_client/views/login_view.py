import tkinter as tk
from tkinter import messagebox

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f0f0f0")

        # Container centralizado
        container = tk.Frame(self, bg="white", padx=40, pady=40, relief="raised", bd=2)
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(container, text="SCEE - Acesso Administrativo", font=("Helvetica", 16, "bold"), bg="white").pack(pady=(0, 20))

        # Campo E-mail
        tk.Label(container, text="E-mail", bg="white", anchor="w").pack(fill="x")
        self.entry_email = tk.Entry(container, width=30, font=("Arial", 12))
        self.entry_email.pack(pady=(0, 10))

        # Campo Senha
        tk.Label(container, text="Senha", bg="white", anchor="w").pack(fill="x")
        self.entry_senha = tk.Entry(container, width=30, font=("Arial", 12), show="*")
        self.entry_senha.pack(pady=(0, 20))

        # Botão Entrar
        btn_entrar = tk.Button(container, text="ENTRAR", bg="#007bff", fg="white", font=("Arial", 10, "bold"),
                               command=self._fazer_login)
        btn_entrar.pack(fill="x", ipady=5)

    def _fazer_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        bridge = self.controller.get_bridge()
        
        # Chama a API via Bridge
        sucesso, mensagem = bridge.login(email, senha)

        if sucesso:
            # Limpa campos
            self.entry_senha.delete(0, tk.END)
            # Navega para o Dashboard
            self.controller.show_frame("DashboardView")
        else:
            messagebox.showerror("Erro de Login", mensagem)