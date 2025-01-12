import tkinter as tk
from random import randint


class Grid:
    def __init__(self, root, size=16, cell_size=30):
        self.root = root
        self.size = size  # Tamaño de la grid (size x size)
        self.cell_size = cell_size  # Tamaño de cada celda en píxeles

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

        # Conjunto de posiciones de comida
        self.food_positions = set()

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
        """Generar comida en una posición aleatoria"""
        while True:
            x = randint(0, self.size - 1)
            y = randint(0, self.size - 1)
            pos = (x, y)
            if pos not in self.food_positions:  # Asegurarse de no duplicar posiciones
                self.food_positions.add(pos)
                self.draw_food(pos)
                break

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
