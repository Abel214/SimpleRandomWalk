from tkinter import Tk, Canvas, Button, Label, Frame
from PIL import Image, ImageTk
import random

# Configuración inicial
WIDTH, HEIGHT = 480, 480  # Dimensiones del área de simulación
STEP = 30  # Tamaño de cada paso de la partícula
TV_INITIAL = 5  # Tiempo de vida inicial de la partícula
FOOD_COUNT = 10  # Número de unidades de comida por ciclo

class ParticleSimulation:
    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='black')  # Lienzo para dibujar
        self.canvas.pack()
        self.tv = TV_INITIAL  # Tiempo de vida de la partícula
        self.food_positions = []  # Posiciones de la comida
        self.particle_position = None  # Posición actual de la partícula
        self.cycle = 0  # Ciclo actual de la simulación
        self.apple_image = None  # Guardar referencia a la imagen
        self.create_ui()
        self.setup_game()

    def create_ui(self):
        # Crear contenedor para usar grid
        self.frame = Frame(self.root, bg='black')
        self.frame.pack()

        self.info_label = Label(self.frame, text="Tiempo de vida: 0 | Ciclo: 0 | Comida: 0",
                                bg='black', fg='white', font=('Arial', 12))
        self.info_label.grid(row=0, column=0, padx=10, pady=10)  # grid para la etiqueta

        self.start_button = Button(self.frame, text="Iniciar", bg='aqua', command=self.start_game)
        self.start_button.grid(row=0, column=1, padx=10)  # grid para el botón

        self.exit_button = Button(self.frame, text="Salir", bg='orange', command=self.salir)
        self.exit_button.grid(row=0, column=2, padx=10)  # grid para el botón


    def setup_game(self):
    # Configuración inicial de la simulación
        self.canvas.delete("all")
        # Dibujar la cuadrícula
        for i in range(0, WIDTH, STEP):
            for j in range(0, HEIGHT, STEP):
                self.canvas.create_rectangle(i, j, i + STEP, j + STEP, fill='gray10')
        
        # Asegurarse de que la partícula y la comida no se salgan de los límites
        self.spawn_particle()  # Crear partícula
        self.spawn_food()  # Generar comida

    def spawn_particle(self):
        # Generar la partícula en uno de los bordes
        edges = [
            (random.randint(0, (WIDTH // STEP) - 1) * STEP, 0),  # Borde superior
            (random.randint(0, (WIDTH // STEP) - 1) * STEP, HEIGHT - STEP),  # Borde inferior
            (0, random.randint(0, (HEIGHT // STEP) - 1) * STEP),  # Borde izquierdo
            (WIDTH - STEP, random.randint(0, (HEIGHT // STEP) - 1) * STEP)  # Borde derecho
        ]
        self.particle_position = random.choice(edges)
        self.tv = TV_INITIAL  # Restablecer el tiempo de vida
        self.canvas.create_oval(self.particle_position[0], self.particle_position[1],
                                self.particle_position[0] + STEP, self.particle_position[1] + STEP,
                                fill="green", tag="particle")

    def spawn_food(self):
        # Cargar la imagen de la manzana solo una vez
        if self.apple_image is None:
            apple_image_pil = Image.open("Files/manzana.jpg")  # Ruta correcta de tu archivo de imagen
            
            # Convertir a modo RGBA (si no lo es) para trabajar con transparencia
            apple_image_pil = apple_image_pil.convert("RGBA")
            
            # Obtener los datos de la imagen
            datas = apple_image_pil.getdata()
            
            # Nueva lista para los datos con transparencia
            new_data = []
            for item in datas:
                # Cambiar todos los píxeles blancos (255, 255, 255) a transparentes
                if item[0] in range(240, 256) and item[1] in range(240, 256) and item[2] in range(240, 256):
                    new_data.append((255, 255, 255, 0))  # Píxel transparente
                else:
                    new_data.append(item)  # Mantener el píxel original
            # Aplicar los cambios a la imagen
            apple_image_pil.putdata(new_data)
            
            # Redimensionar la imagen al tamaño de cada celda (STEP x STEP)
            apple_image_pil = apple_image_pil.resize((STEP, STEP))
            
            # Convertir a formato compatible con Tkinter
            self.apple_image = ImageTk.PhotoImage(apple_image_pil)  

        # Generar comida en posiciones aleatorias dentro de los límites
        self.food_positions = []
        for _ in range(FOOD_COUNT):
            x = random.randint(0, (WIDTH // STEP) - 1) * STEP
            y = random.randint(0, (HEIGHT // STEP) - 1) * STEP
            self.food_positions.append((x, y))
            
            # Colocar la imagen de la manzana en la posición aleatoria
            self.canvas.create_image(x + STEP // 2, y + STEP // 2, image=self.apple_image, tag="food")



    def move_particle(self):
        if self.tv <= 0:  # Si el tiempo de vida se agota
            self.cycle += 1
            self.setup_game()  # Reiniciar ciclo
            return

        # Movimiento aleatorio
        directions = [(0, -STEP), (0, STEP), (-STEP, 0), (STEP, 0)]
        move = random.choice(directions)
        new_position = (self.particle_position[0] + move[0], self.particle_position[1] + move[1])

        # Verificar si el movimiento está dentro de los límites
        if 0 <= new_position[0] < WIDTH and 0 <= new_position[1] < HEIGHT:
            self.particle_position = new_position

        # Actualizar posición de la partícula
        self.canvas.delete("particle")
        self.canvas.create_oval(self.particle_position[0], self.particle_position[1],
                                 self.particle_position[0] + STEP, self.particle_position[1] + STEP,
                                 fill="green", tag="particle")

        # Verificar si la partícula come comida
        if self.particle_position in self.food_positions:
            self.food_positions.remove(self.particle_position)
            self.tv += 5  # Aumentar tiempo de vida al comer
            self.canvas.delete("food")
            self.spawn_food()  # Regenerar comida

        self.tv -= 1  # Reducir tiempo de vida
        self.update_info()
        self.root.after(300, self.move_particle)  # Llamar a la función después de 300 ms

    def update_info(self):
        # Actualizar información de la interfaz
        self.info_label.config(text=f"Tiempo de vida: {self.tv} | Ciclo: {self.cycle} | Comida restante: {len(self.food_positions)}")

    def start_game(self):
        # Iniciar la simulación
        self.cycle = 0
        self.setup_game()
        self.move_particle()

    def salir(self):
        self.root.destroy()

# Crear la ventana principal
root = Tk()
root.title("Simulación de Partícula")
root.geometry(f"{WIDTH}x{HEIGHT + 50}")
root.resizable(False, False)

# Iniciar la simulación
simulation = ParticleSimulation(root)
root.mainloop()
