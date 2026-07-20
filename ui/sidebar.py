import customtkinter as ctk
from .theme import Theme

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, callbacks, **kwargs):
        super().__init__(master, fg_color=Theme.BG_PANEL, width=300, corner_radius=0, **kwargs)
        self.callbacks = callbacks
        self.grid_propagate(False)
        self.entries = {} # Store all input widgets to easily get values
        
        # Tabs principais
        self.tabview = ctk.CTkTabview(self, fg_color=Theme.BG_MAIN, segmented_button_selected_color=Theme.PRIMARY, segmented_button_selected_hover_color=Theme.PRIMARY_HOVER)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("Rasterização")
        self.tabview.add("Curvas")
        self.tabview.add("Polígonos")
        self.tabview.add("Transformações")
        self.tabview.add("Projeções")
        
        # Setup de cada aba
        self.setup_rasterizacao()
        self.setup_curvas()
        self.setup_poligonos()
        self.setup_transformacoes()
        self.setup_projecoes()
        
    def create_card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=Theme.BG_PANEL, corner_radius=8)
        card.pack(fill="x", pady=5, padx=5)
        lbl = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family=Theme.FONT_FAMILY, size=Theme.FONT_SIZE_TEXT, weight="bold"))
        lbl.pack(anchor="w", padx=10, pady=(10, 5))
        return card

    def setup_rasterizacao(self):
        scroll = ctk.CTkScrollableFrame(self.tabview.tab("Rasterização"), fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        # Linha - Bresenham
        card_linha = self.create_card(scroll, "Linha (Bresenham)")
        # Entradas
        row1 = ctk.CTkFrame(card_linha, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=5)
        self.entries['linha_x0'] = ctk.CTkEntry(row1, placeholder_text="X0", width=60)
        self.entries['linha_x0'].pack(side="left", padx=2)
        self.entries['linha_y0'] = ctk.CTkEntry(row1, placeholder_text="Y0", width=60)
        self.entries['linha_y0'].pack(side="left", padx=2)
        
        row2 = ctk.CTkFrame(card_linha, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=5)
        self.entries['linha_x1'] = ctk.CTkEntry(row2, placeholder_text="X1", width=60)
        self.entries['linha_x1'].pack(side="left", padx=2)
        self.entries['linha_y1'] = ctk.CTkEntry(row2, placeholder_text="Y1", width=60)
        self.entries['linha_y1'].pack(side="left", padx=2)
        
        ctk.CTkButton(card_linha, text="Desenhar Linha", command=lambda: self.trigger_callback('linha'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Círculo
        card_circulo = self.create_card(scroll, "Círculo")
        row_c = ctk.CTkFrame(card_circulo, fg_color="transparent")
        row_c.pack(fill="x", padx=10, pady=5)
        self.entries['circulo_cx'] = ctk.CTkEntry(row_c, placeholder_text="CX", width=60)
        self.entries['circulo_cx'].pack(side="left", padx=2)
        self.entries['circulo_cy'] = ctk.CTkEntry(row_c, placeholder_text="CY", width=60)
        self.entries['circulo_cy'].pack(side="left", padx=2)
        self.entries['circulo_r'] = ctk.CTkEntry(row_c, placeholder_text="Raio", width=60)
        self.entries['circulo_r'].pack(side="left", padx=2)
        ctk.CTkButton(card_circulo, text="Desenhar Círculo", command=lambda: self.trigger_callback('circulo'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Elipse
        card_elipse = self.create_card(scroll, "Elipse")
        row_e1 = ctk.CTkFrame(card_elipse, fg_color="transparent")
        row_e1.pack(fill="x", padx=10, pady=5)
        self.entries['elipse_cx'] = ctk.CTkEntry(row_e1, placeholder_text="CX", width=60)
        self.entries['elipse_cx'].pack(side="left", padx=2)
        self.entries['elipse_cy'] = ctk.CTkEntry(row_e1, placeholder_text="CY", width=60)
        self.entries['elipse_cy'].pack(side="left", padx=2)
        row_e2 = ctk.CTkFrame(card_elipse, fg_color="transparent")
        row_e2.pack(fill="x", padx=10, pady=5)
        self.entries['elipse_rx'] = ctk.CTkEntry(row_e2, placeholder_text="Raio X", width=60)
        self.entries['elipse_rx'].pack(side="left", padx=2)
        self.entries['elipse_ry'] = ctk.CTkEntry(row_e2, placeholder_text="Raio Y", width=60)
        self.entries['elipse_ry'].pack(side="left", padx=2)
        ctk.CTkButton(card_elipse, text="Desenhar Elipse", command=lambda: self.trigger_callback('elipse'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

    def setup_curvas(self):
        scroll = ctk.CTkScrollableFrame(self.tabview.tab("Curvas"), fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        card_bezier = self.create_card(scroll, "Curvas de Bézier")
        row_b = ctk.CTkFrame(card_bezier, fg_color="transparent")
        row_b.pack(fill="x", padx=10, pady=5)
        self.entries['curva_x'] = ctk.CTkEntry(row_b, placeholder_text="X", width=60)
        self.entries['curva_x'].pack(side="left", padx=2)
        self.entries['curva_y'] = ctk.CTkEntry(row_b, placeholder_text="Y", width=60)
        self.entries['curva_y'].pack(side="left", padx=2)
        ctk.CTkButton(card_bezier, text="Adicionar Ponto", command=lambda: self.trigger_callback('add_ponto_curva'), fg_color=Theme.BG_MAIN).pack(pady=5, padx=10, fill="x")
        
        self.entries['texto_curvas'] = ctk.CTkTextbox(card_bezier, height=80, fg_color=Theme.BG_MAIN, text_color=Theme.TEXT_MAIN)
        self.entries['texto_curvas'].pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(card_bezier, text="Limpar Pontos", command=lambda: self.trigger_callback('limpar_pontos_curva'), fg_color=Theme.DANGER).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(card_bezier, text="Desenhar Curva", command=lambda: self.trigger_callback('desenhar_curva'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

    def setup_poligonos(self):
        scroll = ctk.CTkScrollableFrame(self.tabview.tab("Polígonos"), fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        # Polilinha
        card_poli = self.create_card(scroll, "Polilinha")
        row_p = ctk.CTkFrame(card_poli, fg_color="transparent")
        row_p.pack(fill="x", padx=10, pady=5)
        self.entries['poli_x'] = ctk.CTkEntry(row_p, placeholder_text="X", width=60)
        self.entries['poli_x'].pack(side="left", padx=2)
        self.entries['poli_y'] = ctk.CTkEntry(row_p, placeholder_text="Y", width=60)
        self.entries['poli_y'].pack(side="left", padx=2)
        ctk.CTkButton(card_poli, text="Adic. Ponto", command=lambda: self.trigger_callback('add_ponto_poli'), fg_color=Theme.BG_MAIN).pack(pady=5, padx=10, fill="x")
        self.entries['texto_poli'] = ctk.CTkTextbox(card_poli, height=60, fg_color=Theme.BG_MAIN)
        self.entries['texto_poli'].pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(card_poli, text="Desenhar Polilinha", command=lambda: self.trigger_callback('desenhar_poli'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Preenchimento Recursivo (Flood Fill)
        card_fill = self.create_card(scroll, "Preenchimento Recursivo")
        ctk.CTkLabel(card_fill, text="1. Desenhe um polígono fechado").pack(anchor="w", padx=10)
        ctk.CTkLabel(card_fill, text="2. Defina semente e cor").pack(anchor="w", padx=10)
        row_fill = ctk.CTkFrame(card_fill, fg_color="transparent")
        row_fill.pack(fill="x", padx=10, pady=5)
        self.entries['fill_x'] = ctk.CTkEntry(row_fill, placeholder_text="Sem X", width=60)
        self.entries['fill_x'].pack(side="left", padx=2)
        self.entries['fill_y'] = ctk.CTkEntry(row_fill, placeholder_text="Sem Y", width=60)
        self.entries['fill_y'].pack(side="left", padx=2)
        self.entries['fill_color'] = ctk.CTkEntry(card_fill, placeholder_text="Cor #RRGGBB")
        self.entries['fill_color'].insert(0, "#FF0000")
        self.entries['fill_color'].pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(card_fill, text="Preencher", command=lambda: self.trigger_callback('preencher'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Varredura
        card_scan = self.create_card(scroll, "Varredura (Scanline)")
        ctk.CTkLabel(card_scan, text="Utiliza os pontos da Polilinha").pack(anchor="w", padx=10)
        ctk.CTkButton(card_scan, text="Preencher Varredura", command=lambda: self.trigger_callback('varredura'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Recorte Linha
        card_clip_l = self.create_card(scroll, "Recorte de Linha")
        ctk.CTkLabel(card_clip_l, text="Janela: xmin, ymin, xmax, ymax").pack(anchor="w", padx=10)
        r_clip1 = ctk.CTkFrame(card_clip_l, fg_color="transparent")
        r_clip1.pack(fill="x", padx=10, pady=2)
        self.entries['clip_xmin'] = ctk.CTkEntry(r_clip1, placeholder_text="xmin", width=40); self.entries['clip_xmin'].pack(side="left", padx=2)
        self.entries['clip_ymin'] = ctk.CTkEntry(r_clip1, placeholder_text="ymin", width=40); self.entries['clip_ymin'].pack(side="left", padx=2)
        self.entries['clip_xmax'] = ctk.CTkEntry(r_clip1, placeholder_text="xmax", width=40); self.entries['clip_xmax'].pack(side="left", padx=2)
        self.entries['clip_ymax'] = ctk.CTkEntry(r_clip1, placeholder_text="ymax", width=40); self.entries['clip_ymax'].pack(side="left", padx=2)
        ctk.CTkLabel(card_clip_l, text="Linha: x0, y0, x1, y1").pack(anchor="w", padx=10)
        r_clip2 = ctk.CTkFrame(card_clip_l, fg_color="transparent")
        r_clip2.pack(fill="x", padx=10, pady=2)
        self.entries['clip_lx0'] = ctk.CTkEntry(r_clip2, placeholder_text="x0", width=40); self.entries['clip_lx0'].pack(side="left", padx=2)
        self.entries['clip_ly0'] = ctk.CTkEntry(r_clip2, placeholder_text="y0", width=40); self.entries['clip_ly0'].pack(side="left", padx=2)
        self.entries['clip_lx1'] = ctk.CTkEntry(r_clip2, placeholder_text="x1", width=40); self.entries['clip_lx1'].pack(side="left", padx=2)
        self.entries['clip_ly1'] = ctk.CTkEntry(r_clip2, placeholder_text="y1", width=40); self.entries['clip_ly1'].pack(side="left", padx=2)
        ctk.CTkButton(card_clip_l, text="Recortar Linha", command=lambda: self.trigger_callback('recorte_linha'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

        # Recorte Polígono
        card_clip_p = self.create_card(scroll, "Recorte de Polígono")
        ctk.CTkLabel(card_clip_p, text="Usa janela acima + pts Polilinha").pack(anchor="w", padx=10)
        ctk.CTkButton(card_clip_p, text="Recortar Polígono", command=lambda: self.trigger_callback('recorte_poligono'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

    def setup_transformacoes(self):
        scroll = ctk.CTkScrollableFrame(self.tabview.tab("Transformações"), fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        card_transf = self.create_card(scroll, "Transformações 2D")
        ctk.CTkLabel(card_transf, text="Utiliza os pontos da Polilinha").pack(anchor="w", padx=10)
        
        ctk.CTkLabel(card_transf, text="Translação (dx, dy)").pack(anchor="w", padx=10, pady=(10,0))
        rt = ctk.CTkFrame(card_transf, fg_color="transparent")
        rt.pack(fill="x", padx=10, pady=2)
        self.entries['trans_dx'] = ctk.CTkEntry(rt, placeholder_text="dx", width=60); self.entries['trans_dx'].pack(side="left", padx=2)
        self.entries['trans_dy'] = ctk.CTkEntry(rt, placeholder_text="dy", width=60); self.entries['trans_dy'].pack(side="left", padx=2)
        ctk.CTkButton(card_transf, text="Aplicar Translação", command=lambda: self.trigger_callback('translacao'), fg_color=Theme.PRIMARY).pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(card_transf, text="Escalonamento (sx, sy)").pack(anchor="w", padx=10, pady=(10,0))
        re = ctk.CTkFrame(card_transf, fg_color="transparent")
        re.pack(fill="x", padx=10, pady=2)
        self.entries['trans_sx'] = ctk.CTkEntry(re, placeholder_text="sx", width=60); self.entries['trans_sx'].pack(side="left", padx=2)
        self.entries['trans_sy'] = ctk.CTkEntry(re, placeholder_text="sy", width=60); self.entries['trans_sy'].pack(side="left", padx=2)
        ctk.CTkLabel(card_transf, text="Pivô (índice do ponto 0-N)").pack(anchor="w", padx=10)
        self.entries['trans_pivo_e'] = ctk.CTkEntry(card_transf, placeholder_text="Pivô", width=60); self.entries['trans_pivo_e'].pack(padx=10, anchor="w")
        ctk.CTkButton(card_transf, text="Aplicar Escala", command=lambda: self.trigger_callback('escala'), fg_color=Theme.PRIMARY).pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(card_transf, text="Rotação (graus)").pack(anchor="w", padx=10, pady=(10,0))
        self.entries['trans_ang'] = ctk.CTkEntry(card_transf, placeholder_text="Ângulo", width=60); self.entries['trans_ang'].pack(padx=10, anchor="w")
        ctk.CTkLabel(card_transf, text="Pivô (índice do ponto 0-N)").pack(anchor="w", padx=10)
        self.entries['trans_pivo_r'] = ctk.CTkEntry(card_transf, placeholder_text="Pivô", width=60); self.entries['trans_pivo_r'].pack(padx=10, anchor="w")
        ctk.CTkButton(card_transf, text="Aplicar Rotação", command=lambda: self.trigger_callback('rotacao'), fg_color=Theme.PRIMARY).pack(pady=5, padx=10, fill="x")

    def setup_projecoes(self):
        scroll = ctk.CTkScrollableFrame(self.tabview.tab("Projeções"), fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        
        card_p = self.create_card(scroll, "Projeção 3D")
        
        # Vertices
        ctk.CTkLabel(card_p, text="Vértice 3D (X, Y, Z)").pack(anchor="w", padx=10)
        rv = ctk.CTkFrame(card_p, fg_color="transparent")
        rv.pack(fill="x", padx=10, pady=2)
        self.entries['proj_x'] = ctk.CTkEntry(rv, placeholder_text="X", width=45); self.entries['proj_x'].pack(side="left", padx=2)
        self.entries['proj_y'] = ctk.CTkEntry(rv, placeholder_text="Y", width=45); self.entries['proj_y'].pack(side="left", padx=2)
        self.entries['proj_z'] = ctk.CTkEntry(rv, placeholder_text="Z", width=45); self.entries['proj_z'].pack(side="left", padx=2)
        ctk.CTkButton(card_p, text="Adic. Vértice", command=lambda: self.trigger_callback('add_vert_3d'), fg_color=Theme.BG_MAIN).pack(pady=5, padx=10, fill="x")
        self.entries['texto_v3d'] = ctk.CTkTextbox(card_p, height=60, fg_color=Theme.BG_MAIN)
        self.entries['texto_v3d'].pack(fill="x", padx=10, pady=5)
        
        # Arestas
        ctk.CTkLabel(card_p, text="Aresta (Índices: De, Para)").pack(anchor="w", padx=10, pady=(10,0))
        ra = ctk.CTkFrame(card_p, fg_color="transparent")
        ra.pack(fill="x", padx=10, pady=2)
        self.entries['proj_ade'] = ctk.CTkEntry(ra, placeholder_text="De", width=60); self.entries['proj_ade'].pack(side="left", padx=2)
        self.entries['proj_apara'] = ctk.CTkEntry(ra, placeholder_text="Para", width=60); self.entries['proj_apara'].pack(side="left", padx=2)
        ctk.CTkButton(card_p, text="Adic. Aresta", command=lambda: self.trigger_callback('add_aresta_3d'), fg_color=Theme.BG_MAIN).pack(pady=5, padx=10, fill="x")
        self.entries['texto_a3d'] = ctk.CTkTextbox(card_p, height=60, fg_color=Theme.BG_MAIN)
        self.entries['texto_a3d'].pack(fill="x", padx=10, pady=5)

        # Config Projeção
        ctk.CTkLabel(card_p, text="Tipo").pack(anchor="w", padx=10, pady=(10,0))
        self.entries['proj_tipo'] = ctk.CTkOptionMenu(card_p, values=["Ortogonal", "Cavalier", "Cabinet", "Perspectiva"], fg_color=Theme.BG_MAIN)
        self.entries['proj_tipo'].pack(fill="x", padx=10, pady=2)
        self.entries['proj_dist'] = ctk.CTkEntry(card_p, placeholder_text="Distância (Persp.)")
        self.entries['proj_dist'].pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(card_p, text="Projetar Objeto", command=lambda: self.trigger_callback('projetar'), fg_color=Theme.PRIMARY).pack(pady=10, padx=10, fill="x")

    def trigger_callback(self, action):
        if action in self.callbacks:
            self.callbacks[action]()

    def get_entry(self, key):
        return self.entries.get(key)
    
    def get_val(self, key, default=None, cast_type=str):
        try:
            val = self.entries.get(key).get()
            return cast_type(val)
        except:
            return default
