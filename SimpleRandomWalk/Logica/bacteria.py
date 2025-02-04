
from random import choice
import tkinter as tk
from tkinter import messagebox

class Bacteria:
    def __init__(self, grid, bacteria_id, steps_per_bacteria, speed=0):
        self.grid = grid
        self.canvas = grid.canvas
        self.cell_size = grid.cell_size
        self.grid_size = grid.size
        self.life_time = steps_per_bacteria + 1
        self.steps_per_bacteria = steps_per_bacteria
        self.num_cycles = 0
        self.max_cycles = 3
        self.initial_move = True
        self.last_position = None
        self.bacteria_id = bacteria_id
        self.is_alive = True
        self.last_position = (0, 0)
        self.has_eaten = False
        self.current_speed = speed
        self.eaten_count = 0
        self.speed_increment_pending = False
        self.waiting_for_others = False
        self.walk_index = 0  # Inicializa el índice del sprite
        self.walk_sprites = []  # Inicializa la lista de sprites
        self.current_direction = None
        self.sprite = None  # Aquí almacenamos el sprite de la bacteria
        self.sprite_update_counter=0
        # Cargar los sprites solo una vez
        self.load_sprites()

        self.create_initial_point()

    def load_sprites(self):
        """Carga los sprites de la bacteria (Walk1.png a Walk10.png)"""
        try:
            # Asegúrate de que estos archivos existen y son accesibles
            self.walk_sprites = []
            for i in range(1, 11):
                sprite_path = f"files/zombie/Walk{i}.png"
                try:
                    sprite = tk.PhotoImage(file=sprite_path)
                    # Mantén una referencia a la imagen para evitar que sea recolectada
                    self.walk_sprites.append(sprite)
                except Exception as e:
                    print(f"Error cargando sprite {i}: {e}")
                    # Usa una imagen de respaldo si no se puede cargar
                    self.walk_sprites.append(None)

            # Verificación más detallada
            if len(self.walk_sprites) != 10 or any(sprite is None for sprite in self.walk_sprites):
                print("Advertencia: No se cargaron todos los sprites correctamente")

        except Exception as e:
            print(f"Error general al cargar los sprites: {e}")

    def load_dead_sprites(self):
        """Carga los sprites de muerte de la bacteria ( Dead1.png)"""
        try:
            # Cargar sprites de muerte
            self.dead_sprites = []
            for i in range(1, 3):  # Asumiendo que hay 2 sprites de muerte
                sprite_path = f"files/zombie/Dead{i}.png"
                try:
                    sprite = tk.PhotoImage(file=sprite_path)
                    # Mantén una referencia a la imagen para evitar que sea recolectada
                    self.dead_sprites.append(sprite)
                except Exception as e:
                    print(f"Error cargando sprite de muerte {i}: {e}")
                    # Usa una imagen de respaldo si no se puede cargar
                    self.dead_sprites.append(None)

            # Verificación más detallada
            if len(self.dead_sprites) != 2 or any(sprite is None for sprite in self.dead_sprites):
                print("Advertencia: No se cargaron todos los sprites de muerte correctamente")

        except Exception as e:
            print(f"Error general al cargar los sprites de muerte: {e}")


    def load_spritesAttack(self):
        """Carga los sprites de la bacteria (Walk1.png a Walk10.png)"""
        try:
            self.walk_sprites = [tk.PhotoImage(file=f"files/zombie/Attack{i}.png") for i in range(1, 3)]
            # Verificar que todos los sprites se cargaron correctamente
            if None in self.walk_sprites:
                raise ValueError("Algunos sprites no se cargaron correctamente.")
        except Exception as e:
            print(f"Error al cargar los sprites: {e}")

    def create_sprite(self):
        """Crear el sprite de la bacteria en el canvas."""
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.walk_sprites[self.walk_index])

    def create_initial_point(self):
        """Crea la bacteria en una de las cuatro esquinas y define su dirección inicial"""
        corners = [(0, 0), (0, self.grid_size - 1),
                   (self.grid_size - 1, 0), (self.grid_size - 1, self.grid_size - 1)]
        self.grid_x, self.grid_y = choice(corners)
        self.last_position = (self.grid_x, self.grid_y)

        # Determinar las direcciones válidas según la esquina
        if self.grid_x == 0 and self.grid_y == 0:  # Esquina superior izquierda
            self.initial_directions = [(0, 1), (1, 0)]  # Solo derecha o abajo
        elif self.grid_x == 0 and self.grid_y == self.grid_size - 1:  # Esquina superior derecha
            self.initial_directions = [(1, 0), (0, -1)]  # Solo abajo o izquierda
        elif self.grid_x == self.grid_size - 1 and self.grid_y == 0:  # Esquina inferior izquierda
            self.initial_directions = [(-1, 0), (0, 1)]  # Solo arriba o derecha
        else:  # Esquina inferior derecha
            self.initial_directions = [(-1, 0), (0, -1)]  # Solo arriba o izquierda

        self.draw_point()
        if self.check_food_collision():
            print(f"Bacteria {self.bacteria_id}: Comió comida en posición inicial ({self.grid_x}, {self.grid_y})")
            self.has_eaten = True
            self.eaten_count += 1
            self.load_spritesAttack()

    def will_collide(self, next_x, next_y):
        """Verifica si habrá colisión en la siguiente posición"""
        # Convertir coordenadas de grid a coordenadas de canvas
        canvas_x = next_x * self.cell_size + self.cell_size // 2
        canvas_y = next_y * self.cell_size + self.cell_size // 2

        # Buscar objetos en la posición siguiente
        overlapping = self.canvas.find_overlapping(
            canvas_x - self.cell_size // 2,
            canvas_y - self.cell_size // 2,
            canvas_x + self.cell_size // 2,
            canvas_y + self.cell_size // 2
        )

        # Verificar si hay otras bacterias en esa posición
        for item_id in overlapping:
            tags = self.canvas.gettags(item_id)
            for tag in tags:
                if tag.startswith('bacteria_') and not tag.endswith(
                        '_text') and not tag == f'bacteria_{self.bacteria_id}':
                    return True
        return False

    def draw_point(self):
        """Dibuja la bacteria en la cuadrícula y su identificador con la animación del sprite"""
        if not self.is_alive:
            return  # No dibujar si está muerta

        # Verificar si los sprites están cargados correctamente
        if not self.walk_sprites:
            print("Error: Los sprites no están cargados.")
            return
        self.walk_index = (self.walk_index + 1) % len(self.walk_sprites)
        # Añadir un contador para controlar la velocidad de animación
        if not hasattr(self, 'sprite_animation_counter'):
            self.sprite_animation_counter = 0
        self.sprite_update_counter += 1
        if self.sprite_update_counter >= 3:  # Cambiar sprite cada 3 frames
            self.walk_index = (self.walk_index + 1) % len(self.walk_sprites)
            self.sprite_update_counter = 0
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size
        self.canvas.delete(f'bacteria_{self.bacteria_id}')  # Eliminar la bacteria anterior
        self.canvas.delete(f'bacteria_{self.bacteria_id}_text')  # Eliminar el texto de la bacteria anterior
        self.canvas.delete(f'bacteria_{self.bacteria_id}_sprite')  # Eliminar el sprite anterior

        # Aquí es donde se dibuja la bacteria con la animación del sprite
        if self.is_alive:
            # Controlar la velocidad de animación
            self.sprite_animation_counter += 1
            if self.sprite_animation_counter >= 5:  # Cambiar sprite cada 5 frames
                # Asegurarse de que walk_index esté dentro del rango válido
                self.walk_index = (self.walk_index + 1) % len(self.walk_sprites)
                self.sprite_animation_counter = 0

            # Dibujar la bacteria usando un sprite (Walk1 a Walk10)
            self.canvas.create_image(
                pixel_x + self.cell_size // 2,  # Centrado en la celda
                pixel_y + self.cell_size // 2,  # Centrado en la celda
                image=self.walk_sprites[self.walk_index],  # Usar el sprite actual
                tag=f'bacteria_{self.bacteria_id}_sprite'  # Etiqueta única para el sprite
            )

            # Dibujar el identificador de la bacteria (el número) encima del sprite
            self.canvas.create_text(
                pixel_x + self.cell_size // 2,  # Centrado en el medio de la celda
                pixel_y + self.cell_size // 2,  # Centrado en el medio de la celda
                text=str(self.bacteria_id),  # El número identificador
                fill='red',  # Color del texto
                font=('Arial', 12, 'bold'),  # Estilo y tamaño de la fuente
                tag=f'bacteria_{self.bacteria_id}_text'  # Etiqueta única para el texto
            )

    def get_valid_moves(self):
        """Determina los movimientos válidos basados en la posición actual"""
        all_directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        valid_moves = []

        for dx, dy in all_directions:
            new_x, new_y = self.grid_x + dx, self.grid_y + dy

            # Verificar que el movimiento:
            # 1. No se salga de la cuadrícula
            # 2. No toque los bordes si no es el movimiento inicial

            if (0 <= new_x < self.grid_size and
                    0 <= new_y < self.grid_size and
                    (self.initial_move or
                     (0 < new_x < self.grid_size - 1 and
                      0 < new_y < self.grid_size - 1))):
                valid_moves.append((dx, dy))

        return valid_moves

    def move(self):
        """Mueve la bacteria con prioridad hacia la comida detectada por radar."""
        if not self.is_alive:
            self.load_dead_sprites()  # Load death sprites
            self.draw_dead_point()  # Draw death animation
            return False

        if self.life_time <= 0:
            print(f"Bacteria {self.bacteria_id}: Vida agotada")
            self.is_alive = False
            return False

        if self.has_eaten and self.life_time == 1:
            self.waiting_for_others = True
            return False
        steps = min(self.current_speed, self.grid_size)  # Limita la velocidad máxima
        for _ in range(steps):
            valid_moves = [move for move in self.get_valid_moves()
                           if not self.will_collide(self.grid_x + move[0], self.grid_y + move[1])]
        # Obtener movimientos válidos
        if self.initial_move:
            valid_moves = []
            for move in self.initial_directions:
                new_x, new_y = self.grid_x + move[0], self.grid_y + move[1]
                if (new_x, new_y) != (self.grid_x, self.grid_y):
                    valid_moves.append(move)
        else:
            valid_moves = [move for move in self.get_valid_moves()
                           if not self.will_collide(self.grid_x + move[0], self.grid_y + move[1])]

        if not valid_moves:
            alternative_direction = self.get_alternative_direction(self.grid_x, self.grid_y)
            if alternative_direction:
                valid_moves = [alternative_direction]
            else:
                self.life_time -= 1
                print(f"Bacteria {self.bacteria_id}: Sin movimientos válidos, vida restante: {self.life_time}")
                if self.life_time <= 0:
                    self.is_alive = False
                    print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
                    self.load_dead_sprites()  # Load death sprites
                    self.draw_dead_point()  # Draw death animation
                return self.is_alive

        # Detectar comida dentro del radio de 2 celdas
        food_positions = self.grid.get_food_within_radius(self.grid_x, self.grid_y, radius=2)
        chosen_move = None
        if food_positions:
            closest_food = min(
                food_positions,
                key=lambda food: abs(food[0] - self.grid_x) + abs(food[1] - self.grid_y)
            )
            dx = closest_food[0] - self.grid_x
            dy = closest_food[1] - self.grid_y
            desired_move = (int(dx / abs(dx)) if dx != 0 else 0,
                            int(dy / abs(dy)) if dy != 0 else 0)

            # Verificar si el movimiento hacia la comida no causa colisión
            if desired_move in valid_moves:
                chosen_move = desired_move
                print(f"Bacteria {self.bacteria_id}: Moviéndose hacia la comida en {closest_food}")

        if not chosen_move:
            chosen_move = choice(valid_moves)
            print(f"Bacteria {self.bacteria_id}: Movimiento aleatorio por una colision cercana")
        self.last_position = (self.grid_x, self.grid_y)
        self.grid_x += chosen_move[0]
        self.grid_y += chosen_move[1]

        # Verificar colisión con comida
        if self.check_food_collision():
            print(f"Bacteria {self.bacteria_id}: Comió comida en ({self.grid_x}, {self.grid_y})")
            self.has_eaten = True
            self.eaten_count += 1
            self.load_spritesAttack()
            if self.eaten_count >= 2 and self.current_speed < 2:
                self.speed_increment_pending = True
                print(f"Bacteria {self.bacteria_id}: Velocidad pendiente para el próximo ciclo")

        # Mover múltiples pasos según la velocidad actual
        for _ in range(self.current_speed):
            next_x = self.grid_x + chosen_move[0]
            next_y = self.grid_y + chosen_move[1]

            # Solo moverse si no hay colisión
            if not self.will_collide(next_x, next_y):
                self.grid_x = next_x
                self.grid_y = next_y
                if self.check_food_collision():
                    print(f"Bacteria {self.bacteria_id}: Comió comida en ({self.grid_x}, {self.grid_y})")
                    self.has_eaten = True
                    self.eaten_count += 1

        # Dibujar el punto con animación
        self.draw_point()
        self.life_time -= 1
        if self.life_time <= 0:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
            self.load_dead_sprites()  # Load death sprites
            self.draw_dead_point()  # Draw death animation
        else:
            print(f"Bacteria {self.bacteria_id}: Vida restante: {self.life_time}")

        return self.is_alive

    def pass_to_next_cycle(self):
        self.num_cycles += 1
        print(f"Bacteria {self.bacteria_id}: Iniciando ciclo {self.num_cycles}")
        root = tk.Tk()
        root.withdraw()  # Oculta la ventana principal
        print("Bacterias Sobrevivientes",
                            f"Bacteria {self.bacteria_id}: Iniciando ciclo {self.num_cycles}")

        # Si comió dos comidas, incrementar velocidad
        if self.eaten_count >= 2:
            self.current_speed += 1
            print(f"Bacteria {self.bacteria_id}: Velocidad aumentada a {self.current_speed}")
            # Mostrar alerta al usuario
            root = tk.Tk()
            root.withdraw()  # Oculta la ventana principal
            print("Incremento de Velocidad",
                                f"La bacteria {self.bacteria_id} ha incrementado su velocidad a {self.current_speed}.")

        # Resetear el contador de comidas
        self.eaten_count = 0

        if self.num_cycles >= self.max_cycles:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta por alcanzar el límite de ciclos.")
            return False

        # Modificar la condición de supervivencia
        # Si ha comido al menos una vez en el ciclo anterior, sigue viva
        if not self.has_eaten:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta porque no comió.")
            return False

        # Reset life and parameters for the new cycle
        self.life_time = self.steps_per_bacteria + 1
        self.has_eaten = False
        self.initial_move = True

        self.create_initial_point()

        return True

    def reset_for_next_cycle(self):
        """Reset parameters at the start of a new cycle."""
        self.eaten_count = 0
        self.speed_increment_pending = False
        self.has_eaten = False

    def check_food_collision(self):
        """Comprueba si la bacteria colisiona con comida"""
        current_pos = (self.grid_x, self.grid_y)
        if current_pos in self.grid.food_positions:
            self.grid.food_positions.remove(current_pos)
            self.grid.canvas.delete('food')
            self.grid.redraw_food()
            self.has_eaten = True
            # self.last_position = current_pos
            return True
        return False

    def get_alternative_direction(self, current_x, current_y):
        """Obtiene una dirección alternativa cuando hay colisión"""
        possible_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # derecha, abajo, izquierda, arriba
        valid_directions = []

        for dx, dy in possible_directions:
            next_x = current_x + dx
            next_y = current_y + dy

            # Verificar si la nueva dirección está dentro de los límites
            if (0 <= next_x < self.grid_size and
                    0 <= next_y < self.grid_size and
                    not self.will_collide(next_x, next_y)):

                # Si estamos en el movimiento inicial o no hay dirección actual, aceptar cualquier dirección válida
                if self.initial_move or self.current_direction is None:
                    valid_directions.append((dx, dy))
                # Si no es movimiento inicial, evitar retroceder
                elif (dx, dy) != (-self.current_direction[0], -self.current_direction[1]):
                    valid_directions.append((dx, dy))

        return choice(valid_directions) if valid_directions else None

    def draw_dead_point(self):
        """Dibuja los sprites de muerte de la bacteria"""
        if not self.is_alive and hasattr(self, 'dead_sprites'):
            # Verificar si los sprites de muerte están cargados correctamente
            if not self.dead_sprites:
                print("Error: Los sprites de muerte no están cargados.")
                return

            # Añadir un contador para controlar la velocidad de animación de los sprites de muerte
            if not hasattr(self, 'dead_sprite_animation_counter'):
                self.dead_sprite_animation_counter = 0

            self.dead_sprite_animation_counter += 1
            dead_sprite_index = (self.dead_sprite_animation_counter // 5) % len(self.dead_sprites)

            pixel_x = self.grid_x * self.cell_size
            pixel_y = self.grid_y * self.cell_size

            # Eliminar sprites anteriores
            self.canvas.delete(f'bacteria_{self.bacteria_id}')
            self.canvas.delete(f'bacteria_{self.bacteria_id}_text')
            self.canvas.delete(f'bacteria_{self.bacteria_id}_sprite')

            # Dibujar la bacteria usando un sprite de muerte
            self.canvas.create_image(
                pixel_x + self.cell_size // 2,  # Centrado en la celda
                pixel_y + self.cell_size // 2,  # Centrado en la celda
                image=self.dead_sprites[dead_sprite_index],  # Usar el sprite de muerte actual
                tag=f'bacteria_{self.bacteria_id}_sprite'  # Etiqueta única para el sprite
            )