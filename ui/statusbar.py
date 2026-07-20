import customtkinter as ctk
from .theme import Theme

class Statusbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Theme.BG_PANEL, height=30, corner_radius=0, **kwargs)
        self.grid_propagate(False)
        
        font_style = ctk.CTkFont(family=Theme.FONT_FAMILY, size=Theme.FONT_SIZE_SMALL)
        
        # Ferramenta Atual
        self.lbl_tool = ctk.CTkLabel(self, text="Ferramenta: Nenhuma", font=font_style, text_color=Theme.TEXT_SEC)
        self.lbl_tool.pack(side="left", padx=15)
        
        # Coordenadas do Mouse
        self.lbl_coords = ctk.CTkLabel(self, text="X: 0 | Y: 0", font=font_style, text_color=Theme.TEXT_MAIN)
        self.lbl_coords.pack(side="left", padx=15)
        
        # Zoom
        self.lbl_zoom = ctk.CTkLabel(self, text="Zoom: 100%", font=font_style, text_color=Theme.TEXT_SEC)
        self.lbl_zoom.pack(side="left", padx=15)
        
        # Status do Poligono/Pontos
        self.lbl_points = ctk.CTkLabel(self, text="Pontos: 0", font=font_style, text_color=Theme.TEXT_SEC)
        self.lbl_points.pack(side="right", padx=15)
        
    def set_tool(self, tool_name):
        self.lbl_tool.configure(text=f"Ferramenta: {tool_name}")
        
    def set_coords(self, x, y):
        self.lbl_coords.configure(text=f"X: {x} | Y: {y}")
        
    def set_zoom(self, zoom_value):
        zoom_pct = int(zoom_value * 100)
        self.lbl_zoom.configure(text=f"Zoom: {zoom_pct}%")
        
    def set_points_count(self, count):
        self.lbl_points.configure(text=f"Pontos: {count}")
