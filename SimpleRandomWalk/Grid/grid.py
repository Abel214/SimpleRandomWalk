import tkinter as tk
from random import randint, choice
from PIL import Image, ImageTk

class Grid:
    def __init__(self, root, size=20, cell_size=30):  # Aumenté el tamaño de la grid a 32x32
        self.root = root
        self.size = size  # Tamaño de la grid (size x size)
        self.cell_size = cell_size  # Tamaño de cada celda en píxeles
        self.food_positions = set()  # Conjunto de posiciones de comidas
        # Calcular dimensiones totales
        self.width = self.size * self.cell_size
        self.height = self.size * self.cell_size
        self.bg_image = None
        self.load_food_sprites()
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

    def load_food_sprites(self):
        try:
            self.food_sprites = []
            for i in range(1, 11):
                try:
                    sprite_path = f"files/zombie/Food{i}.png"
                    # Resize the image to a smaller size
                    original_sprite = tk.PhotoImage(file=sprite_path)
                    # Resize to a smaller dimension, e.g., 20x20 pixels
                    smaller_sprite = original_sprite.subsample(2, 2)  # Divides size by 2
                    self.food_sprites.append(smaller_sprite)
                except Exception as e:
                    self.food_sprites.append(None)
        except Exception as e:
            print(f"General error loading food sprites: {e}")

    def draw_food(self, position, sprite_index=0):
        x, y = position
        pixel_x = x * self.cell_size
        pixel_y = y * self.cell_size

        if hasattr(self, 'food_sprites') and 0 <= sprite_index < len(self.food_sprites):
            sprite = self.food_sprites[sprite_index]
            if sprite is not None:
                # Position the smaller sprite more centrally
                return self.canvas.create_image(
                    pixel_x + self.cell_size // 2,
                    pixel_y + self.cell_size // 2,
                    image=sprite,
                    tag='food'
                )

        # Fallback remains the same
        padding = self.cell_size // 4
        return self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='red',
            tag='food'
        )
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

    def load_background(self, image_path):
        """Carga y coloca la imagen de fondo en el Canvas."""
        try:
            image = Image.open(image_path)
            image = image.resize((self.width, self.height))  # Ajusta al tamaño del canvas
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except Exception as e:
            print(f"Error al cargar la imagen de fondo: {e}")
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


    def find_nearest_food(self, x, y, radius=2):
        """Buscar la comida más cercana dentro del radio especificado."""
        nearest_food = None
        shortest_distance = float('inf')

        for food_x, food_y in self.food_positions:
            distance = abs(food_x - x) + abs(food_y - y)
            if distance <= radius and distance < shortest_distance:
                nearest_food = (food_x, food_y)
                shortest_distance = distance

        return nearest_food

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
        Dibujar un rectángulo o círculo en la nueva posición de la bacteria.
        """
        # Etiqueta única para identificar la bacteria en el canvas
        tag = f'bacteria_{bacteria_id}'

        # Elimina la representación previa de la bacteria
        self.canvas.delete(tag)

        # Calcular coordenadas para dibujar la bacteria
        pixel_x = new_x * self.cell_size
        pixel_y = new_y * self.cell_size
        padding = self.cell_size // 6

        # Dibujar la nueva posición de la bacteria
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='green',
            tag=tag
        )
