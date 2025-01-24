from random import choice
class Bacteria:
    def __init__(self, grid, bacteria_id, steps_per_bacteria, speed=0):
        self.grid = grid
        self.canvas = grid.canvas
        self.cell_size = grid.cell_size
        self.grid_size = grid.size
        self.life_time = steps_per_bacteria + 1
        self.steps_per_bacteria = steps_per_bacteria
        self.num_cycles = 0
        self.max_cycles = 6
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
        self.create_initial_point()

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

    def draw_point(self):
        """Dibuja la bacteria en la cuadrícula y su identificador sin dejar rastro"""
        if not self.is_alive:
            return  # No dibujar si está muerta
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size
        self.canvas.delete(f'bacteria_{self.bacteria_id}')  # Eliminar el círculo de la bacteria anterior
        self.canvas.delete(f'bacteria_{self.bacteria_id}_text')  # Eliminar el texto de la bacteria anterior
        padding = self.cell_size // 4

        # Aquí es donde se dibuja la bacteria en la cuadrícula
        if self.is_alive:
            # Dibujar la bacteria como un círculo
            self.canvas.create_oval(
                pixel_x + padding,
                pixel_y + padding,
                pixel_x + self.cell_size - padding,
                pixel_y + self.cell_size - padding,
                fill='green',
                tag=f'bacteria_{self.bacteria_id}'  # Usamos el ID como tag único
            )

            # Dibujar el identificador de la bacteria (el número) encima del círculo
            self.canvas.create_text(
                pixel_x + self.cell_size // 2,  # Centrado en el medio de la celda
                pixel_y + self.cell_size // 2,  # Centrado en el medio de la celda
                text=str(self.bacteria_id),  # El número identificador
                fill='white',  # Color del texto
                font=('Arial', 8, 'bold'),  # Estilo y tamaño de la fuente
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
        """Mueve la bacteria con restricciones de movimiento y mecánica de velocidad."""
        if not self.is_alive:
            self.grid.canvas.delete(f'bacteria_{self.bacteria_id}')
            self.grid.canvas.delete(f'bacteria_{self.bacteria_id}_text')
            return False

        if self.life_time <= 0:
            print(f"Bacteria {self.bacteria_id}: Vida agotada")
            self.is_alive = False
            return False

        if self.has_eaten and self.life_time == 1:
            self.waiting_for_others = True
            return False

        # Obtain valid moves
        if self.initial_move:
            valid_moves = []
            for move in self.initial_directions:
                new_x, new_y = self.grid_x + move[0], self.grid_y + move[1]
                if (new_x, new_y) != (self.grid_x, self.grid_y):
                    valid_moves.append(move)
        else:
            valid_moves = self.get_valid_moves()

        if not valid_moves:
            self.life_time -= 1
            print(f"Bacteria {self.bacteria_id}: Sin movimientos válidos, vida restante: {self.life_time}")
            if self.life_time <= 0:
                self.is_alive = False
                print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
            return self.is_alive

        move = choice(valid_moves)
        self.last_position = (self.grid_x, self.grid_y)
        self.grid_x += move[0]
        self.grid_y += move[1]

        # Check for food collision
        if self.check_food_collision():
            print(f"Bacteria {self.bacteria_id}: Comió comida en ({self.grid_x}, {self.grid_y})")
            self.has_eaten = True
            self.eaten_count += 1
            # Update speed mechanism
            if self.eaten_count >= 2 and self.current_speed < 2:
                self.speed_increment_pending = True
                print(f"Bacteria {self.bacteria_id}: Velocidad pendiente para el próximo ciclo")

        # Move multiple steps based on current speed
        for _ in range(self.current_speed):
            self.grid_x += move[0]
            self.grid_y += move[1]
            if self.check_food_collision():
                print(f"Bacteria {self.bacteria_id}: Comió comida en ({self.grid_x}, {self.grid_y})")
                self.has_eaten = True
                self.eaten_count += 1

        # Draw the point in the new position
        self.draw_point()
        self.initial_move = False

        # Reduce life
        self.life_time -= 1
        if self.life_time <= 0:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
        else:
            print(f"Bacteria {self.bacteria_id}: Vida restante: {self.life_time}")

        return self.is_alive

    def pass_to_next_cycle(self):
        self.num_cycles += 1
        print(f"Bacteria {self.bacteria_id}: Iniciando ciclo {self.num_cycles}")

        # Si comió dos comidas, incrementar velocidad
        if self.eaten_count >= 2:
            self.current_speed += 1
            print(f"Bacteria {self.bacteria_id}: Velocidad aumentada a {self.current_speed}")

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


