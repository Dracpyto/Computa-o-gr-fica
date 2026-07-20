import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from .theme import Theme
from .toolbar import Toolbar
from .statusbar import Statusbar
from .sidebar import Sidebar
from .canvas import ModernCanvas

# Importando Algoritmos Matemáticos Puros (sem alterar)
from Sistemas.bresenham import Bresenham
from Sistemas.polilinha import Polilinha
from Sistemas.circulo import Circulo
from Sistemas.elipse import Elipse
from Sistemas.curvas import Curvas
from Sistemas.preenchimentoRecursivo import PreenchimentoRecursivo
from Sistemas.varredura import Varredura
from Sistemas.recorteLinha import RecorteLinha
from Sistemas.recortePoligono import RecortePoligono
from Sistemas.transformacao import Transformacao
from Sistemas.projecoes import Projetor3D

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Theme.BG_MAIN, **kwargs)
        
        self.pack(fill="both", expand=True)
        
        # Grid Configuration
        self.grid_rowconfigure(1, weight=1) # Row 1 holds Sidebar and Canvas, needs to expand
        self.grid_columnconfigure(1, weight=1) # Column 1 holds Canvas, needs to expand
        
        # Callbacks Map
        tb_callbacks = {
            'clear': self.clear_all,
            'reset': self.reset_view,
            'export': self.export_image
        }
        
        sb_callbacks = {
            'linha': self.cmd_linha,
            'circulo': self.cmd_circulo,
            'elipse': self.cmd_elipse,
            'add_ponto_curva': self.cmd_add_ponto_curva,
            'limpar_pontos_curva': self.cmd_limpar_pontos_curva,
            'desenhar_curva': self.cmd_desenhar_curva,
            'add_ponto_poli': self.cmd_add_ponto_poli,
            'desenhar_poli': self.cmd_desenhar_poli,
            'preencher': self.cmd_preencher,
            'varredura': self.cmd_varredura,
            'recorte_linha': self.cmd_recorte_linha,
            'recorte_poligono': self.cmd_recorte_poligono,
            'translacao': self.cmd_translacao,
            'escala': self.cmd_escala,
            'rotacao': self.cmd_rotacao,
            'add_vert_3d': self.cmd_add_vert_3d,
            'add_aresta_3d': self.cmd_add_aresta_3d,
            'projetar': self.cmd_projetar
        }
        
        # Componentes
        self.toolbar = Toolbar(self, callbacks=tb_callbacks)
        self.toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.sidebar = Sidebar(self, callbacks=sb_callbacks)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        
        self.statusbar = Statusbar(self)
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")
        
        self.canvas = ModernCanvas(
            self, 
            statusbar_callback=self.on_canvas_move,
            click_callback=self.on_canvas_click,
            matrix_size=100
        )
        self.canvas.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # --- ESTADO GLOBAL DA APLICAÇÃO ---
        self.pontos_selecionados = []
        self.poligono_atual = [] # Para transformações e varredura
        self.vertices_3d = []
        self.arestas_3d = []
        
        self.statusbar.set_tool("Nenhuma (Passe o mouse)")

    def init_globals(self):
        self.pontos_selecionados = []
        self.poligono_atual = []
        self.vertices_3d = []
        self.arestas_3d = []
        self.atualizar_textos()

    def atualizar_textos(self):
        # Limpa os Textboxes
        tb_curva = self.sidebar.get_entry('texto_curvas')
        tb_poli = self.sidebar.get_entry('texto_poli')
        
        # Helper para não dar erro
        def upd(tb, arr):
            if tb:
                tb.configure(state="normal")
                tb.delete("1.0", "end")
                for p in arr:
                    tb.insert("end", f"({int(p[0])}, {int(p[1])})\n")
                tb.configure(state="disabled")
                
        upd(tb_curva, self.pontos_selecionados)
        upd(tb_poli, self.poligono_atual)
        
        self.statusbar.set_points_count(len(self.pontos_selecionados) + len(self.poligono_atual))

    # --- CANVAS EVENT HANDLERS ---
    def on_canvas_move(self, x, y, zoom):
        self.statusbar.set_coords(x, y)
        self.statusbar.set_zoom(zoom)
        
    def on_canvas_click(self, x, y):
        # Aqui poderiamos implementar a captura rapida de pontos,
        # mas como simplificação da conversão, vamos apenas notificar 
        # as coordenas para o usuario digitar. Se quiser clique -> ponto 
        # precisa setar o modo. Vamos deixar como log para agora, e priorizar entradas.
        # Adicionar visualmente um marcador onde clicou
        self.canvas.draw_temp_marker(x, y, Theme.COLOR_TEMP)

    # --- BARRA DE FERRAMENTAS ---
    def clear_all(self):
        self.init_globals()
        self.canvas.clear()
        
    def reset_view(self):
        self.canvas.offset_x = 0
        self.canvas.offset_y = 0
        self.canvas.zoom = 1.0
        self.canvas.redraw_grid()
        self.statusbar.set_zoom(1.0)
        
    def export_image(self):
        try:
            from PIL import ImageGrab
            # Export basic screen grab of the canvas area
            x = self.canvas.canvas.winfo_rootx()
            y = self.canvas.canvas.winfo_rooty()
            w = self.canvas.canvas.winfo_width()
            h = self.canvas.canvas.winfo_height()
            
            img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
            img.save("export.png")
            messagebox.showinfo("Sucesso", "Imagem exportada como export.png")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar (Pillow/Ghostscript necessário): {str(e)}")

    # --- COMANDOS DOS ALGORITMOS (Via Entradas) ---
    def cmd_linha(self):
        self.statusbar.set_tool("Bresenham")
        x0 = self.sidebar.get_val('linha_x0', cast_type=int)
        y0 = self.sidebar.get_val('linha_y0', cast_type=int)
        x1 = self.sidebar.get_val('linha_x1', cast_type=int)
        y1 = self.sidebar.get_val('linha_y1', cast_type=int)
        
        if None in (x0, y0, x1, y1):
            messagebox.showerror("Erro", "Valores inválidos.")
            return
            
        linha = Bresenham((x0, y0), (x1, y1))
        self.canvas.draw_pixels(linha.saida, Theme.COLOR_LINE)
        # Destacar os pontos
        self.canvas.draw_pixel(x0, y0, Theme.COLOR_CONTROL_POINT)
        self.canvas.draw_pixel(x1, y1, Theme.COLOR_CONTROL_POINT)

    def cmd_circulo(self):
        self.statusbar.set_tool("Círculo")
        cx = self.sidebar.get_val('circulo_cx', cast_type=int)
        cy = self.sidebar.get_val('circulo_cy', cast_type=int)
        r = self.sidebar.get_val('circulo_r', cast_type=float)
        
        if None in (cx, cy, r) or r <= 0:
            messagebox.showerror("Erro", "Valores inválidos.")
            return
            
        circ = Circulo((cx, cy), r)
        self.canvas.draw_pixels(circ.saida, Theme.COLOR_LINE)
        self.canvas.draw_pixel(cx, cy, Theme.COLOR_CENTER)

    def cmd_elipse(self):
        self.statusbar.set_tool("Elipse")
        cx = self.sidebar.get_val('elipse_cx', cast_type=int)
        cy = self.sidebar.get_val('elipse_cy', cast_type=int)
        rx = self.sidebar.get_val('elipse_rx', cast_type=float)
        ry = self.sidebar.get_val('elipse_ry', cast_type=float)
        
        if None in (cx, cy, rx, ry) or rx <= 0 or ry <= 0:
            messagebox.showerror("Erro", "Valores inválidos.")
            return
            
        eli = Elipse((cx, cy), rx, ry)
        self.canvas.draw_pixels(eli.saida, Theme.COLOR_LINE)
        self.canvas.draw_pixel(cx, cy, Theme.COLOR_CENTER)

    def cmd_add_ponto_curva(self):
        x = self.sidebar.get_val('curva_x', cast_type=int)
        y = self.sidebar.get_val('curva_y', cast_type=int)
        if None in (x, y):
            messagebox.showerror("Erro", "Valores inválidos.")
            return
        self.pontos_selecionados.append((x, y))
        self.canvas.draw_pixel(x, y, Theme.COLOR_CONTROL_POINT)
        self.sidebar.get_entry('curva_x').delete(0, 'end')
        self.sidebar.get_entry('curva_y').delete(0, 'end')
        self.atualizar_textos()

    def cmd_limpar_pontos_curva(self):
        self.pontos_selecionados = []
        self.atualizar_textos()

    def cmd_desenhar_curva(self):
        self.statusbar.set_tool("Curva Bézier")
        if len(self.pontos_selecionados) < 3:
            messagebox.showerror("Erro", "Pelo menos 3 pontos.")
            return
        curva = Curvas(self.pontos_selecionados)
        self.canvas.draw_pixels(curva.saida, Theme.COLOR_CURVE)

    def cmd_add_ponto_poli(self):
        x = self.sidebar.get_val('poli_x', cast_type=int)
        y = self.sidebar.get_val('poli_y', cast_type=int)
        if None in (x, y):
            messagebox.showerror("Erro", "Valores inválidos.")
            return
        self.poligono_atual.append((x, y))
        self.canvas.draw_pixel(x, y, Theme.COLOR_CONTROL_POINT)
        self.sidebar.get_entry('poli_x').delete(0, 'end')
        self.sidebar.get_entry('poli_y').delete(0, 'end')
        self.atualizar_textos()

    def cmd_desenhar_poli(self, fechar=True):
        self.statusbar.set_tool("Polilinha")
        if len(self.poligono_atual) < 2:
            messagebox.showerror("Erro", "Pelo menos 2 pontos.")
            return
        poli = Polilinha(self.poligono_atual, fechar=fechar)
        self.canvas.draw_pixels(poli.saida, Theme.COLOR_POLYGON)
        
    def cmd_preencher(self):
        self.statusbar.set_tool("Flood Fill")
        x = self.sidebar.get_val('fill_x', cast_type=int)
        y = self.sidebar.get_val('fill_y', cast_type=int)
        cor = self.sidebar.get_val('fill_color', cast_type=str)
        
        if None in (x, y) or not cor:
            messagebox.showerror("Erro", "Valores inválidos.")
            return
            
        if len(self.poligono_atual) < 3:
            messagebox.showerror("Erro", "Desenhe um polígono primeiro (Polilinha + fechar).")
            return
            
        # Garante o poligono desenhado
        self.cmd_desenhar_poli(fechar=True)
        # Executa flood fill
        # Usa propria classe de preenchimento, modificando para passar a funçao de checar pixel
        # Devido as amarras da arquitetura do Flood Fill original que recebia a "tela" inteira
        # vamos usar um adapter inline.
        
        # Patch the PreenchimentoRecursivo to use our check/draw
        import sys
        sys.setrecursionlimit(5000)
        
        class TelaAdapter:
            def __init__(self, c):
                self.c = c
            def checar_matriz(self, gx, gy):
                color = self.c.check_matrix_color(gx, gy)
                return color if color else "#000000" # fallback para borda virtual
            def desenhar_pixel(self, gx, gy, c):
                self.c.draw_pixel(gx, gy, c)
                
        adapter = TelaAdapter(self.canvas)
        PreenchimentoRecursivo((x, y), cor, adapter)

    def cmd_varredura(self):
        self.statusbar.set_tool("Varredura")
        if len(self.poligono_atual) < 3:
            messagebox.showerror("Erro", "Defina o polígono primeiro.")
            return
            
        varr = Varredura(self.poligono_atual)
        self.canvas.draw_pixels(varr.saida, Theme.COLOR_POLYGON)
        self.cmd_desenhar_poli(fechar=True) # Redesenha a borda

    def cmd_recorte_linha(self):
        self.statusbar.set_tool("Recorte de Linha")
        xmin = self.sidebar.get_val('clip_xmin', cast_type=int)
        ymin = self.sidebar.get_val('clip_ymin', cast_type=int)
        xmax = self.sidebar.get_val('clip_xmax', cast_type=int)
        ymax = self.sidebar.get_val('clip_ymax', cast_type=int)
        
        x0 = self.sidebar.get_val('clip_lx0', cast_type=int)
        y0 = self.sidebar.get_val('clip_ly0', cast_type=int)
        x1 = self.sidebar.get_val('clip_lx1', cast_type=int)
        y1 = self.sidebar.get_val('clip_ly1', cast_type=int)
        
        if None in (xmin, ymin, xmax, ymax, x0, y0, x1, y1):
            return
            
        self.canvas.clear()
        
        janela = {'xmin': min(xmin, xmax), 'ymin': min(ymin, ymax), 'xmax': max(xmin, xmax), 'ymax': max(ymin, ymax)}
        self.canvas.highlight_clip_window(**janela)
        
        linha_orig = Bresenham((x0, y0), (x1, y1))
        self.canvas.draw_pixels(linha_orig.saida, Theme.COLOR_GRID) # Original fraca
        
        rec = RecorteLinha((x0, y0), (x1, y1), **janela)
        self.canvas.draw_pixels(rec.saida, Theme.COLOR_LINE)
        
    def cmd_recorte_poligono(self):
        self.statusbar.set_tool("Recorte de Polígono")
        xmin = self.sidebar.get_val('clip_xmin', cast_type=int)
        ymin = self.sidebar.get_val('clip_ymin', cast_type=int)
        xmax = self.sidebar.get_val('clip_xmax', cast_type=int)
        ymax = self.sidebar.get_val('clip_ymax', cast_type=int)
        
        if None in (xmin, ymin, xmax, ymax) or len(self.poligono_atual) < 3:
            return
            
        self.canvas.clear()
        janela = {'xmin': min(xmin, xmax), 'ymin': min(ymin, ymax), 'xmax': max(xmin, xmax), 'ymax': max(ymin, ymax)}
        self.canvas.highlight_clip_window(**janela)
        
        poli_orig = Polilinha(self.poligono_atual, fechar=True)
        self.canvas.draw_pixels(poli_orig.saida, Theme.COLOR_GRID)
        
        rec = RecortePoligono(self.poligono_atual, **janela)
        self.canvas.draw_pixels(rec.saida, Theme.COLOR_POLYGON)

    def cmd_translacao(self):
        self.statusbar.set_tool("Translação")
        dx = self.sidebar.get_val('trans_dx', cast_type=int)
        dy = self.sidebar.get_val('trans_dy', cast_type=int)
        if None in (dx, dy) or not self.poligono_atual: return
        
        trans = Transformacao(self.poligono_atual)
        self.poligono_atual = trans.translacao(dx, dy)
        self.atualizar_textos()
        self.canvas.clear()
        self.cmd_desenhar_poli(fechar=True)
        
    def cmd_escala(self):
        self.statusbar.set_tool("Escalonamento")
        sx = self.sidebar.get_val('trans_sx', cast_type=float)
        sy = self.sidebar.get_val('trans_sy', cast_type=float)
        idx_pivo = self.sidebar.get_val('trans_pivo_e', cast_type=int)
        if None in (sx, sy) or not self.poligono_atual: return
        
        pivo = self.poligono_atual[idx_pivo] if (idx_pivo is not None and 0 <= idx_pivo < len(self.poligono_atual)) else None
        
        trans = Transformacao(self.poligono_atual)
        pixels = trans.escalonamento(sx, sy, pivo=pivo)
        
        self.canvas.clear()
        self.canvas.draw_pixels(pixels, Theme.COLOR_RESULT)
        # O retorno nao eh mais uma lista de vertices, e sim pixels rasterizados de acordo c a engine original,
        # portanto nao podemos atualizar o self.poligono_atual com eles

    def cmd_rotacao(self):
        self.statusbar.set_tool("Rotação")
        ang = self.sidebar.get_val('trans_ang', cast_type=float)
        idx_pivo = self.sidebar.get_val('trans_pivo_r', cast_type=int)
        if ang is None or not self.poligono_atual: return
        
        pivo = self.poligono_atual[idx_pivo] if (idx_pivo is not None and 0 <= idx_pivo < len(self.poligono_atual)) else None
        
        trans = Transformacao(self.poligono_atual)
        pixels = trans.rotacao(ang, pivo=pivo)
        
        self.canvas.clear()
        self.canvas.draw_pixels(pixels, Theme.COLOR_RESULT)

    def cmd_add_vert_3d(self):
        x = self.sidebar.get_val('proj_x', cast_type=int)
        y = self.sidebar.get_val('proj_y', cast_type=int)
        z = self.sidebar.get_val('proj_z', cast_type=int)
        if None in (x, y, z): return
        
        self.vertices_3d.append([x, y, z])
        self.sidebar.get_entry('proj_x').delete(0, 'end')
        self.sidebar.get_entry('proj_y').delete(0, 'end')
        self.sidebar.get_entry('proj_z').delete(0, 'end')
        
        tb = self.sidebar.get_entry('texto_v3d')
        tb.configure(state="normal")
        tb.insert("end", f"V{len(self.vertices_3d)-1}: ({x}, {y}, {z})\n")
        tb.configure(state="disabled")

    def cmd_add_aresta_3d(self):
        de = self.sidebar.get_val('proj_ade', cast_type=int)
        para = self.sidebar.get_val('proj_apara', cast_type=int)
        if None in (de, para): return
        
        if 0 <= de < len(self.vertices_3d) and 0 <= para < len(self.vertices_3d):
            self.arestas_3d.append([de, para])
            tb = self.sidebar.get_entry('texto_a3d')
            tb.configure(state="normal")
            tb.insert("end", f"Aresta: V{de} -- V{para}\n")
            tb.configure(state="disabled")

    def cmd_projetar(self):
        self.statusbar.set_tool("Projeção 3D")
        tipo = self.sidebar.get_val('proj_tipo', cast_type=str)
        dist = self.sidebar.get_val('proj_dist', cast_type=int)
        if not self.vertices_3d or not self.arestas_3d: return
        
        self.canvas.clear()
        projetor = Projetor3D(self.vertices_3d, self.arestas_3d)
        
        if tipo == "Ortogonal":
            proj = projetor.projecao_ortogonal()
        elif tipo == "Cavalier":
            proj = projetor.projecao_obliqua(45, 1.0)
        elif tipo == "Cabinet":
            proj = projetor.projecao_obliqua(45, 0.5)
        elif tipo == "Perspectiva":
            proj = projetor.projecao_perspectiva(dist if dist else 20)
        else:
            return
            
        self.canvas.draw_pixels(proj, Theme.COLOR_RESULT)
