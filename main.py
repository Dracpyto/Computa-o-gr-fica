import customtkinter as ctk
from ui.main_window import MainWindow

def main():
    # Configuração Inicial do CustomTkinter
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = ctk.CTk()
    app.title("Sistema de Computação Gráfica")
    
    # Define um tamanho inicial que faz sentido (eixo maior para o canvas)
    app.geometry("1200x800")
    app.minsize(1000, 600)
    
    # Injeta o MainWindow no root
    main_window = MainWindow(app)
    
    app.mainloop()

if __name__ == "__main__":
    main()