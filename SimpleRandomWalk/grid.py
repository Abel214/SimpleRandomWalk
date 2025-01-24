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
    
    # Busca posiciones de comida dentro de un radio específico
    def get_food_within_radius(self, x, y, radius):
        """Devuelve una lista de posiciones de comida dentro del radio especificado."""
        food_positions = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                # Verificar si la posición está dentro de los límites y contiene comida
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) in self.food_positions:
                    food_positions.append((nx, ny))
        return food_positions

    def consume_food(self, x, y):
        """
        Consume comida en la posición (x, y) si existe.
        Devuelve True si había comida y se consumió, de lo contrario, False.
        """
        position = (x, y)
        if position in self.food_positions:
            self.food_positions.remove(position)
            self.redraw_food()  # Actualizar el canvas para eliminar la comida consumida
            return True
        return False

    def update_bacteria_position(self, bacteria_id, new_x, new_y):
        """
        Actualiza la posición de una bacteria en el canvas.
        Dibuja un círculo (bacteria) y su identificador (texto) en la nueva posición.
        """
        # Etiqueta única para identificar la bacteria en el canvas
        tag = f'bacteria_{bacteria_id}'
        
        # Elimina la representación previa de la bacteria y su texto
        self.canvas.delete(tag)
        self.canvas.delete(f'bacteria_{bacteria_id}_text')
        
        # Calcular coordenadas para dibujar la bacteria
        pixel_x = new_x * self.cell_size
        pixel_y = new_y * self.cell_size
        padding = self.cell_size // 4  # Ajuste del relleno según la celda
        
        # Dibujar la nueva posición de la bacteria
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='green',
            tag=tag  # Usamos el ID como tag único
        )
        
        # Dibujar el identificador de la bacteria (el número) encima del círculo
        self.canvas.create_text(
            pixel_x + self.cell_size // 2,  # Centrado en el medio de la celda
            pixel_y + self.cell_size // 2,  # Centrado en el medio de la celda
            text=str(bacteria_id),  # El número identificador
            fill='white',  # Color del texto
            font=('Arial', 8, 'bold'),  # Estilo y tamaño de la fuente
            tag=f'bacteria_{bacteria_id}_text'  # Etiqueta única para el texto
        )




