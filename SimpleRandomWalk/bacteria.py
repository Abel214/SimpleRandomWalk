from random import choice

class Bacteria:
    def __init__(self, grid, bacteria_id,steps_per_bacteria):
        self.grid = grid
        self.canvas = grid.canvas
        self.cell_size = grid.cell_size
        self.grid_size = grid.size
        self.life_time = steps_per_bacteria +1
        self.steps_per_bacteria = steps_per_bacteria
        self.num_cycles = 0
        self.max_cycles = 3
        self.initial_move = True
        self.last_position = None
        self.bacteria_id = bacteria_id  # Aquí asignamos el bacteria_id
        self.is_alive = True  # Estado inicial de la bacteria
        self.last_position = (0, 0)
        self.has_eaten = False
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
        """Mueve la bacteria con restricciones de movimiento."""
        if not self.is_alive:
            self.canvas.delete()
            print(f"Bacteria {self.bacteria_id}: Muerta")
            return False  # No se mueve si está muerta

        if self.life_time <= 0:  # Cuando la vida de la bacteria llega a 0 no se mueve
            print(f"Bacteria {self.bacteria_id}: Vida agotada")
            self.is_alive = False
            # Eliminar la bacteria del canvas cuando se agota su vida
            self.canvas.delete()
            return False
        if self.has_eaten and self.life_time == 1:
            self.waiting_for_others = True  # La bacteria ya no espera
            return False
        # Obtener movimientos válidos según la situación
        if self.initial_move:
            valid_moves = []
            # Verificar si el primer movimiento no lleva a la posición inicial
            for move in self.initial_directions:
                new_x, new_y = self.grid_x + move[0], self.grid_y + move[1]
                if (new_x, new_y) != (self.grid_x, self.grid_y):  # Evitar regresar a la posición inicial
                    valid_moves.append(move)
        else:
            valid_moves = self.get_valid_moves()

        # Si no hay movimientos válidos, pierde vida
        if not valid_moves:
            self.life_time -= 1
            print(f"Bacteria {self.bacteria_id}: Sin movimientos válidos, vida restante: {self.life_time}")
            if self.life_time <= 0:
                self.is_alive = False
                print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
                self.canvas.delete()
            return self.is_alive

        # Seleccionar un movimiento aleatorio entre los válidos
        move = choice(valid_moves)

        # Guardar la posición actual antes de mover
        self.last_position = (self.grid_x, self.grid_y)

        # Realizar el movimiento
        self.grid_x += move[0]
        self.grid_y += move[1]

        # Verificar colisión con comida
        if self.check_food_collision():
            print(f"Bacteria {self.bacteria_id}: Comió comida en ({self.grid_x}, {self.grid_y})")
            self.has_eaten = True

            # Verificar si la vida es 1 después de comer, y detener si es así
            if self.life_time == 1:
                print(f"Bacteria {self.bacteria_id}: Se detiene al llegar a 1 paso después de comer.")
                self.waiting_for_others = False  # Cambiar el estado de espera a False
                return False  # Detenerse porque la vida está en 1

        # Dibujar el punto en la nueva posición
        self.draw_point()
        self.initial_move = False

        # Reducir vida y verificar si debe morir
        self.life_time -= 1
        if self.life_time <= 0:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta por inanición")
        else:
            print(f"Bacteria {self.bacteria_id}: Vida restante: {self.life_time}")

        return self.is_alive

    def check_food_collision(self):
        """Comprueba si la bacteria colisiona con comida"""
        current_pos = (self.grid_x, self.grid_y)
        if current_pos in self.grid.food_positions:
            self.grid.food_positions.remove(current_pos)
            self.grid.canvas.delete('food')
            self.grid.redraw_food()
            self.has_eaten = True
            #self.last_position = current_pos
            return True
        return False

    def pass_to_next_cycle(self):
        self.num_cycles += 1
        print(f"Bacteria {self.bacteria_id}: Iniciando ciclo {self.num_cycles}")

        if self.num_cycles >= self.max_cycles:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta por alcanzar el límite de ciclos.")
            return False

        if not self.has_eaten:
            self.is_alive = False
            print(f"Bacteria {self.bacteria_id}: Muerta porque no comió.")
            return False

        # Reiniciar los pasos y el estado para el nuevo ciclo
        self.life_time = self.steps_per_bacteria + 1
        self.has_eaten = False
        self.initial_move = True

        # Si la bacteria comió, su última posición será donde comió

        self.create_initial_point()

        return True

