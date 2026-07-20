import tkinter as tk
import math
import customtkinter as ctk
from .theme import Theme

class ModernCanvas(ctk.CTkFrame):
    """
    Canvas avançado com suporte a Pan, Zoom e Grid dinâmico.
    Mantém uma matriz abstrata para operações matemáticas como Flood Fill.
    """
    def __init__(self, master, statusbar_callback=None, click_callback=None, matrix_size=100, **kwargs):
        super().__init__(master, fg_color=Theme.BG_CANVAS, **kwargs)
        
        self.statusbar_callback = statusbar_callback
        self.click_callback = click_callback
        
        # O Canvas padrão do Tkinter embedded
        self.canvas = tk.Canvas(self, bg=Theme.BG_CANVAS, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Variáveis de Transformação da Câmera (Pan e Zoom)
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.pixel_size = 20 # Tamanho base de uma unidade de grade em pixels da tela
        
        # Variáveis para o Pan
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        # Matriz abstrata para preenchimento
        self.matrix_size = matrix_size
        self.abstract_matrix = [[None for _ in range(matrix_size)] for _ in range(matrix_size)]
        
        # Bindings
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Zoom (Windows e Linux/Mac)
        self.canvas.bind("<MouseWheel>", self.on_zoom)
        self.canvas.bind("<Button-4>", self.on_zoom)
        self.canvas.bind("<Button-5>", self.on_zoom)
        
        # Pan (Arrasto com botão do meio ou direito)
        self.canvas.bind("<Button-2>", self.on_pan_start)
        self.canvas.bind("<B2-Motion>", self.on_pan_drag)
        self.canvas.bind("<Button-3>", self.on_pan_start)
        self.canvas.bind("<B3-Motion>", self.on_pan_drag)
        
        # Clique Principal
        self.canvas.bind("<Button-1>", self.on_left_click)

    # --- SISTEMA DE COORDENADAS ---
    def get_center_screen(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return w / 2, h / 2

    def to_screen_coords(self, grid_x, grid_y):
        """Converte de coordenadas abstratas do grid para pixels na tela (aplicando zoom e pan)"""
        cx, cy = self.get_center_screen()
        actual_pixel_size = self.pixel_size * self.zoom
        
        screen_x = cx + self.offset_x + (grid_x * actual_pixel_size)
        screen_y = cy + self.offset_y - (grid_y * actual_pixel_size) # Y inverte no canvas
        return screen_x, screen_y

    def to_grid_coords(self, screen_x, screen_y):
        """Converte pixels na tela de volta para o grid abstrato inteiro"""
        cx, cy = self.get_center_screen()
        actual_pixel_size = self.pixel_size * self.zoom
        
        # Aplica a fórmula inversa
        grid_x = (screen_x - cx - self.offset_x) / actual_pixel_size
        grid_y = (cy + self.offset_y - screen_y) / actual_pixel_size
        
        # Arredonda para encontrar a "célula" clicada
        return math.floor(grid_x), math.floor(grid_y)

    def to_matrix_index(self, grid_x, grid_y):
        """Converte coordenadas da grade abstrata (centrada em 0,0) para índices da matriz interna (0 a N)"""
        col = int(grid_x + (self.matrix_size / 2))
        row = int((self.matrix_size / 2) - grid_y - 1)
        return row, col

    def is_in_matrix_bounds(self, grid_x, grid_y):
        limit = self.matrix_size / 2
        return -limit <= grid_x < limit and -limit <= grid_y < limit

    # --- EVENTOS DE CÂMERA E MOUSE ---
    def on_resize(self, event):
        self.redraw_grid()

    def on_zoom(self, event):
        # Diferentes OS disparam wheel differently
        if event.num == 4 or getattr(event, 'delta', 0) > 0:
            zoom_factor = 1.1
        elif event.num == 5 or getattr(event, 'delta', 0) < 0:
            zoom_factor = 0.9
        else:
            return

        # Limitar zoom
        new_zoom = self.zoom * zoom_factor
        if 0.1 < new_zoom < 20.0:
            # Aproxima em direção ao centro da tela
            self.zoom = new_zoom
            self.redraw_grid()
            
            if self.statusbar_callback:
                # Dispara atualização de zoom
                pass # A barra de status busca isso do parent

    def on_pan_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_pan_drag(self, event):
        dx = event.x - self._drag_start_x
        dy = event.y - self._drag_start_y
        self.offset_x += dx
        self.offset_y += dy
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self.redraw_grid()

    def on_mouse_move(self, event):
        grid_x, grid_y = self.to_grid_coords(event.x, event.y)
        if self.statusbar_callback:
            self.statusbar_callback(grid_x, grid_y, self.zoom)

    def on_left_click(self, event):
        grid_x, grid_y = self.to_grid_coords(event.x, event.y)
        if self.click_callback:
            self.click_callback(grid_x, grid_y)

    # --- DESENHO ---
    def redraw_grid(self):
        self.canvas.delete("grid")
        self.canvas.delete("axis")
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1: return
        
        actual_pixel_size = self.pixel_size * self.zoom
        
        cx, cy = self.get_center_screen()
        origin_x = cx + self.offset_x
        origin_y = cy + self.offset_y
        
        # Linhas Verticais
        start_x = origin_x % actual_pixel_size
        for x in range(int(start_x), w, int(actual_pixel_size)):
            width = 2 if abs(x - origin_x) < 1 else 1
            color = Theme.COLOR_AXIS_Y if width == 2 else Theme.COLOR_GRID
            tag = "axis" if width == 2 else "grid"
            self.canvas.create_line(x, 0, x, h, fill=color, width=width, tags=tag)
            
        # Linhas Horizontais
        start_y = origin_y % actual_pixel_size
        for y in range(int(start_y), h, int(actual_pixel_size)):
            width = 2 if abs(y - origin_y) < 1 else 1
            color = Theme.COLOR_AXIS_X if width == 2 else Theme.COLOR_GRID
            tag = "axis" if width == 2 else "grid"
            self.canvas.create_line(0, y, w, y, fill=color, width=width, tags=tag)
            
        # Redesenhar todos os objetos renderizados - para simplificar a demo e o desempenho
        # Os objetos seriam redesenhados aqui pelo main_window baseando-se no estado.
        # Mas para ser compativel com o sistema antigo que nao salva primitivas complexas, 
        # nos precisamos que main_window ou app_callbacks force redraw dos itens q ele controla.

    def clear(self):
        self.canvas.delete("all")
        self.abstract_matrix = [[None for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.redraw_grid()

    def draw_pixel(self, grid_x, grid_y, color, tag="draw"):
        # Pinta na matriz abstrata se estiver dentro dos limites (usado apenas pelo Flood Fill)
        if self.is_in_matrix_bounds(grid_x, grid_y):
            row, col = self.to_matrix_index(grid_x, grid_y)
            self.abstract_matrix[row][col] = color
        
        # Pinta na tela visualmente (infinito)
        x1, y1 = self.to_screen_coords(grid_x, grid_y)
        actual_size = self.pixel_size * self.zoom
        
        # Se x1, y1 for o centro superior esquerdo do pixel abstrato:
        # Ponto (0,0) vai de (origin_x, origin_y - size) a (origin_x + size, origin_y)
        self.canvas.create_rectangle(
            x1, y1 - actual_size, 
            x1 + actual_size, y1, 
            fill=color, outline=color, tags=tag
        )

    def draw_pixels(self, points, color, tag="draw"):
        for p in points:
            self.draw_pixel(p[0], p[1], color, tag)

    def draw_temp_marker(self, grid_x, grid_y, color):
        x1, y1 = self.to_screen_coords(grid_x, grid_y)
        actual_size = self.pixel_size * self.zoom
        self.canvas.create_oval(
            x1 + 2, y1 - actual_size + 2, 
            x1 + actual_size - 2, y1 - 2, 
            fill=color, outline="", tags="temp_marker"
        )

    def clear_temp_markers(self):
        self.canvas.delete("temp_marker")

    def highlight_clip_window(self, xmin, ymin, xmax, ymax):
        # A janela vai do pixel inferior esquerdo ao superior direito
        x1, y1 = self.to_screen_coords(xmin, ymax)
        x2, y2 = self.to_screen_coords(xmax + 1, ymin - 1)
        # O xmax+1 e ymin-1 garantem englobar os blocos dos pixels
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=Theme.DANGER, width=2, tags="clip_window")

    def check_matrix_color(self, grid_x, grid_y):
        if not self.is_in_matrix_bounds(grid_x, grid_y):
            return "#000000" # Considera fora como borda preta
        row, col = self.to_matrix_index(grid_x, grid_y)
        color = self.abstract_matrix[row][col]
        return color if color is not None else None
