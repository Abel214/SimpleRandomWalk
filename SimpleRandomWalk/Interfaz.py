import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk


ventana_principal = Tk()  # Crear una ventana
ventana_principal.title("Menú Juego de Simple Random Walk")
ventana_principal.minsize(width=800, height=600)  # Establecer el tamaño mínimo de la ventana
ventana_principal.config(padx=0, pady=0)

# Obtener las dimensiones de la pantalla
pantalla_ancho = ventana_principal.winfo_screenwidth()
pantalla_alto = ventana_principal.winfo_screenheight()

# Establecer el tamaño deseado para la ventana
ventana_ancho = 850
ventana_alto = 600

# Calcular las coordenadas para centrar la ventana
pos_x = 430
pos_y = 90

# Establecer la geometría de la ventana con la posición calculada y el tamaño deseado
ventana_principal.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")

# Cargar una imagen de fondo (.gif o .ppm)
ruta_imagen = "files/snakeInterfaz.gif"
gif_imagen = Image.open(ruta_imagen)

# Crear un Canvas para el fondo
canvas = Canvas(ventana_principal, width=ventana_ancho, height=ventana_alto)
canvas.pack(fill="both", expand=True)

# Lista para guardar los fotogramas del GIF
fotogramas = []
try:
    while True:
        # Redimensionar cada fotograma del GIF al tamaño de la ventana
        fotograma = gif_imagen.copy()
        fotograma = fotograma.resize((ventana_ancho, ventana_alto), Image.Resampling.LANCZOS)
        fotogramas.append(ImageTk.PhotoImage(fotograma))
        gif_imagen.seek(len(fotogramas))  # Ir al siguiente fotograma
except EOFError:
    pass  # Se llegó al final del GIF

# Mostrar el primer fotograma en el Canvas
imagen_fondo = canvas.create_image(0, 0, image=fotogramas[0], anchor="nw")


# Función para animar el GIF
def animar_fondo(indice=0):
    frame_actual = fotogramas[indice]
    canvas.itemconfig(imagen_fondo, image=frame_actual)
    indice = (indice + 1) % len(fotogramas)  # Ciclar los fotogramas
    ventana_principal.after(50, animar_fondo, indice)  # Cambiar cada 50 ms


# Iniciar la animación
animar_fondo()

barra_menu = Menu(ventana_principal)
ventana_principal.config(menu=barra_menu)


def salir():
    resp = messagebox.askquestion("Salir", "¿Desea salir del juego?")
    if resp == 'yes':
        ventana_principal.destroy()


def acerca_de():
    messagebox.showinfo("Acerca de", "Desarrollado por: Brian Aguinsaca y Abel Mora")


def ventana_JuegoCartas():
    ventana_principal.withdraw()



# Menú
menu_inicio = tkinter.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Inicio", menu=menu_inicio)
menu_inicio.add_command(label="Salir", command=salir)

menu_operaciones = tkinter.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Operaciones", menu=menu_operaciones)
menu_operaciones.add_command(label="Simple Random Walk", command=ventana_JuegoCartas)


menu_ayuda = tkinter.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
menu_ayuda.add_command(label="Acerca de", command=acerca_de)

ventana_principal.mainloop()
