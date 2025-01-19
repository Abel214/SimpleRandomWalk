import tkinter as tk
from random import randint, choice

class Grid:
    def __init__(self, root, size=16, cell_size=30):
        self.root = root
        self.size = size  # Tamaño de la grid (size x size)
        self.cell_size = cell_size  # Tamaño de cada celda en píxeles
        self.food_positions = set()  # Conjunto de posiciones de comidas
        # Calcular dimensiones totales
        self.width = self.size * self.cell_size
        self.height = self.size * self.cell_size

        # Crear el canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg='black'
        )
        self.canvas.pack(pady=10)

        # Crear la grid visual
        self.create_grid()

    def create_grid(self):
        """Crear la cuadrícula visual"""
        # Líneas verticales
        for i in range(0, self.width + 1, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.height,
                fill='gray20'
            )

        # Líneas horizontales
        for i in range(0, self.height + 1, self.cell_size):
            self.canvas.create_line(
                0, i, self.width, i,
                fill='gray20'
            )

    def spawn_food(self):
        """Genera una nueva comida en una posición aleatoria vacía"""
        while True:
            x = choice(range(self.size))
            y = choice(range(self.size))
            position = (x, y)

            # Asegura que la comida no reaparezca en una posición ya ocupada
            if position not in self.food_positions:
                self.food_positions.add(position)
                self.draw_food(position)
                break

    def spawn_initial_food(self, num_food=10):
        """Genera un número inicial de comidas aleatorias"""
        self.canvas.delete('food')  # Elimina todas las comidas anteriores, si es necesario
        self.food_positions.clear()  # Limpiar todas las posiciones de comida para regenerarlas

        # Genera comidas nuevas
        for _ in range(num_food):
            self.spawn_food()

    def redraw_food(self):
        """Redibuja todas las comidas que no han sido consumidas"""
        self.canvas.delete('food')  # Borra todas las comidas
        for position in self.food_positions:
            self.draw_food(position)

    def draw_food(self, position):
        """Dibujar comida en el canvas"""
        x, y = position
        pixel_x = x * self.cell_size
        pixel_y = y * self.cell_size
        padding = self.cell_size // 4
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='red',
            tag='food'
        )


