import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk  # Importa Pillow

from SimpleRandomWalk.UI.panelJuego import PanelJuego


class Intermedio:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal

        # Crear ventana emergente
        self.ventana_intermedia = Toplevel(ventana_principal)
        self.ventana_intermedia.title("Selecciona tu Bioma")
        ventana_principal.minsize(width=400, height=400)  # Establecer el tamaño mínimo de la ventana
        ventana_principal.config(padx=0, pady=0)

        # Obtener las dimensiones de la pantalla
        pantalla_ancho = ventana_principal.winfo_screenwidth()
        pantalla_alto = ventana_principal.winfo_screenheight()

        # Establecer el tamaño deseado para la ventana
        ventana_ancho = 800
        ventana_alto = 400

        # Calcular las coordenadas para centrar la ventana
        pos_x = (pantalla_ancho - ventana_ancho) // 2
        pos_y = (pantalla_alto - ventana_alto) // 2

        # Establecer la geometría de la ventana con la posición calculada y el tamaño deseado
        self.ventana_intermedia.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")

        # Cargar imágenes de los biomas (con PIL para JPG/PNG)
        self.bg_left = Image.open("files/biomaInvierno.jpg")
        self.bg_left = self.bg_left.resize((400, 500))  # Redimensionar si es necesario
        self.bg_left = ImageTk.PhotoImage(self.bg_left)

        self.bg_right = Image.open("files/biomaDesierto.jpg")
        self.bg_right = self.bg_right.resize((400, 500))
        self.bg_right = ImageTk.PhotoImage(self.bg_right)
        # Canvas para colocar imágenes
        self.canvas = tk.Canvas(self.ventana_intermedia, width=800, height=400)
        # Centrar el canvas, puedes modificar estos valores para moverlo según lo necesites
        self.canvas.place(relx=0.5, rely=0.4, anchor='center')

        # Mostrar imágenes en los lados
        self.canvas.create_image(200, 200, image=self.bg_left)
        self.canvas.create_image(600, 200, image=self.bg_right)

        # Botones para seleccionar el bioma
        self.btn_left = tk.Button(self.ventana_intermedia, text="Bioma Invierno", command=self.seleccionar_invierno)
        self.btn_left.place(x=150, y=350)

        self.btn_right = tk.Button(self.ventana_intermedia, text="Bioma Desierto", command=self.seleccionar_desierto)
        self.btn_right.place(x=550, y=350)

        # Botón para regresar al menú
        self.btn_volver = tk.Button(self.ventana_intermedia, text="Volver al Menú", command=self.volver_menu)
        self.btn_volver.place(x=370, y=350)

    def seleccionar_invierno(self):
        self.ventana_intermedia.withdraw()
        print("Bioma de Invierno seleccionado")
        num_bacterias = 1
        num_food = 10
        steps_per_bacteria = 6
        panel_juego = PanelJuego(self.ventana_principal, self.ventana_intermedia, num_bacterias, num_food,
                                 steps_per_bacteria)
        panel_juego.abrir_ventana("files/War2.png")


    def seleccionar_desierto(self):
        self.ventana_intermedia.withdraw()
        print("Bioma de Desierto seleccionado")
        num_bacterias = 2
        num_food = 30
        steps_per_bacteria = 6
        panel_juego = PanelJuego(self.ventana_principal, self.ventana_intermedia, num_bacterias, num_food,
                                 steps_per_bacteria)
        panel_juego.abrir_ventana("files/War.png")


    def volver_menu(self):
        self.ventana_intermedia.destroy()  # Cierra la ventana intermedia
        self.ventana_principal.deiconify()  # Muestra la ventana principal nuevamente
