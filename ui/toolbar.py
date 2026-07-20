import customtkinter as ctk
from .theme import Theme

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, fg_color=Theme.BG_PANEL, height=50, corner_radius=0, **kwargs)
        self.callbacks = callbacks
        self.grid_propagate(False)
        
        # Título / Logo
        title_lbl = ctk.CTkLabel(
            self, 
            text="Sistema de Computação Gráfica", 
            font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=Theme.FONT_SIZE_TITLE, weight="bold"),
            text_color=Theme.TEXT_MAIN
        )
        title_lbl.pack(side="left", padx=20, pady=10)
        
        # Ações Globais (Alinhadas à direita)
        btn_export = ctk.CTkButton(
            self, 
            text="Exportar Imagem", 
            command=self.callbacks.get('export', lambda: None),
            fg_color=Theme.SUCCESS,
            hover_color=Theme.PRIMARY_HOVER,
            width=120
        )
        btn_export.pack(side="right", padx=10, pady=10)
        
        btn_reset = ctk.CTkButton(
            self, 
            text="Resetar Visão", 
            command=self.callbacks.get('reset', lambda: None),
            fg_color=Theme.BG_MAIN,
            hover_color=Theme.BG_PANEL,
            border_width=1,
            border_color=Theme.TEXT_SEC,
            text_color=Theme.TEXT_MAIN,
            width=100
        )
        btn_reset.pack(side="right", padx=10, pady=10)
        
        btn_clear = ctk.CTkButton(
            self, 
            text="Limpar Canvas", 
            command=self.callbacks.get('clear', lambda: None),
            fg_color=Theme.DANGER,
            hover_color=Theme.DANGER_HOVER,
            width=100
        )
        btn_clear.pack(side="right", padx=10, pady=10)
        
        self.theme_switch = ctk.CTkSwitch(
            self, 
            text="Tema Claro", 
            command=self.toggle_theme,
            progress_color=Theme.PRIMARY
        )
        self.theme_switch.pack(side="right", padx=20, pady=10)
        
    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
