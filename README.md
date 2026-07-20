# Sistema de Computação Gráfica

Uma aplicação profissional e moderna de Computação Gráfica interativa desenvolvida em Python. O sistema permite desenhar e manipular primitivas gráficas 2D e projetar objetos 3D com uma interface visual limpa, baseada em [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), com funcionalidades avançadas de navegação (Pan e Zoom infinitos).

## ✨ Funcionalidades

O sistema implementa puramente os algoritmos matemáticos de rasterização clássicos sem depender de engines externas de desenho:

*   **Rasterização Básica**: Desenho de Linhas (Bresenham), Círculos e Elipses.
*   **Polígonos**: Criação de Polilinhas (fechadas ou abertas).
*   **Curvas**: Desenho de Curvas de Bézier.
*   **Preenchimento**: Algoritmo de Varredura (Scanline) e Flood Fill (Recursivo).
*   **Recortes (Clipping)**: Recorte de Linha (Cohen-Sutherland) e Recorte de Polígono (Sutherland-Hodgman).
*   **Transformações 2D**: Translação, Rotação e Escalonamento em relação à origem ou a um ponto pivô arbitrário.
*   **Projeções 3D**: Projeções de vértices e arestas nos formatos Ortogonal, Cavalier, Cabinet e Perspectiva.

## 🚀 Arquitetura

O projeto está dividido entre a Lógica de Negócio (Matemática Pura) e a Camada de Apresentação (Interface CustomTkinter):

*   `Sistemas/`: Contém os arquivos isolados com as lógicas de rasterização que recebem pontos ideais e devolvem listas de pixels mapeados.
*   `ui/`: Diretório contendo a interface moderna.
    *   `canvas.py`: Uma classe super carregada estendendo o TKinter Canvas que adiciona controle de câmera, arrasto, scale wheel e gerencia conversões de espaço virtual matematico de coordendas para tela visual do usuário.
    *   `sidebar.py`, `statusbar.py`, `toolbar.py`: Estruturas visuais desacopladas da matemática.
    *   `main_window.py`: O Controlador que coordena as entradas do usuário, o estado global da aplicação e envia os resultados da pasta `Sistemas/` para serem pintados pelo Canvas.
*   `main.py`: Ponto de entrada do sistema.

## 🛠️ Instalação e Execução

### Pré-requisitos
*   Python 3.11 ou superior
*   Bibliotecas especificadas

### Passos
1. Clone este repositório:
   ```bash
   git clone https://github.com/Dracpyto/Computa-o-gr-fica.git
   ```
2. Entre na pasta do projeto:
   ```bash
   cd Computa-o-gr-fica
   ```
3. Instale as dependências visuais (`customtkinter` para a interface e `pillow` para a capacidade de exportar imagens do Canvas):
   ```bash
   pip install customtkinter pillow
   ```
4. Inicie o sistema:
   ```bash
   python main.py
   ```

## 👨‍💻 Controles da Câmera (Mouse)

*   **Zoom In / Zoom Out**: Use a Roda de Rolagem (*Scroll Wheel*).
*   **Pan (Arrastar a tela)**: Segure o botão do meio (bolinha do mouse) ou o botão direito do mouse e arraste para navegar pelo plano cartesiano infinito.

---
**Desenvolvido por:** Adan Mafra (Dracpyto)
