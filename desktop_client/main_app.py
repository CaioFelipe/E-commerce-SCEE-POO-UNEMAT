import tkinter as tk
from tkinter import messagebox
from controllers.bridge import BridgeController

# Importação das Views
from views.login_view import LoginView
from views.dashboard_view import DashboardView

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SCEE - Gestão Desktop (Ana)")
        self.geometry("1024x768")
        
        # Instancia o controlador de API (Ponte)
        self.bridge = BridgeController()
        
        # Container Principal
        # Usamos pack aqui para colocar o container na janela principal
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        
        # Configuração do Grid para o Container
        # Isso permite que as telas (frames) sejam empilhadas umas sobre as outras
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Inicializa todas as telas e as empilha usando GRID
        for F in (LoginView, DashboardView):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            
            # O erro acontecia porque aqui usamos grid(), mas o Label antigo usava pack()
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Removemos o Label temporário que causava o conflito pack vs grid
        
        # Começa exibindo a tela de Login
        self.show_frame("LoginView")

    def show_frame(self, page_name):
        """Traz uma view para o topo da pilha."""
        frame = self.frames[page_name]
        
        # Se a view tiver lógica de "On Show" (como carregar dados), dispara evento
        frame.event_generate("<<Show>>")
        
        frame.tkraise()

    def get_bridge(self):
        """Permite que as Views acessem a bridge."""
        return self.bridge

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()