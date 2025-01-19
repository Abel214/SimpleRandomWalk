from random import choice

class Bacteria:
    def __init__(self, grid, bacteria_id):
        self.grid = grid
        self.canvas = grid.canvas
        self.cell_size = grid.cell_size
        self.grid_size = grid.size
        self.life_time = 6
        self.num_cycles = 0
        self.max_cycles = 3
        self.initial_move = True
        self.last_position = None
        self.bacteria_id = bacteria_id  # Aquí asignamos el bacteria_id
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
        """Dibuja la bacteria en la cuadrícula."""
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size
        self.canvas.delete(f'bacteria_{self.bacteria_id}')  # Usa el ID para identificar cada bacteria
        padding = self.cell_size // 4
        # Aquí es donde se dibuja la bacteria en la cuadrícula, sin llamada recursiva
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='green',
            tag=f'bacteria_{self.bacteria_id}'  # Usamos el ID como tag único
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

    def draw_point(self):
        """Dibuja la bacteria en la cuadrícula."""
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size
        self.canvas.delete(f'bacteria_{self.bacteria_id}')  # Usa el ID para identificar cada bacteria
        padding = self.cell_size // 4
        # Aquí es donde se dibuja la bacteria en la cuadrícula, sin llamada recursiva
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='green',
            tag=f'bacteria_{self.bacteria_id}'  # Usamos el ID como tag único
        )

    def move(self):
        """Mueve la bacteria con restricciones de movimiento"""
        if self.life_time <= 0:  # cuando la vida de la bacteria llega a 0 no se mueve
            return False

        # Obtener movimientos válidos según la situación
        if self.initial_move:
            valid_moves = []
            # Verificar si el primer movimiento no lleva a la posición inicial
            for move in self.initial_directions:
                new_x, new_y = self.grid_x + move[0], self.grid_y + move[1]
                # Asegurarse de que no regrese a la posición inicial
                if (new_x, new_y) != (self.grid_x, self.grid_y):
                    valid_moves.append(move)

        else:
            valid_moves = self.get_valid_moves()

        # Si no hay movimientos válidos, mantener la posición actual
        if not valid_moves:
            self.life_time -= 1
            return True

        # Seleccionar un movimiento aleatorio entre los válidos
        move = choice(valid_moves)

        # Guardar la posición actual antes de mover
        self.last_position = (self.grid_x, self.grid_y)

        # Realizar el movimiento
        self.grid_x += move[0]
        self.grid_y += move[1]

        if self.check_food_collision():
            return self.pass_to_next_cycle()

        self.draw_point()
        self.initial_move = False

        self.life_time -= 1  # Cada vez que se mueve, se debe restar uno de la vida

        return True

    def check_food_collision(self):
        """Comprueba si la bacteria colisiona con comida"""
        current_pos = (self.grid_x, self.grid_y)
        if current_pos in self.grid.food_positions:
            self.grid.food_positions.remove(current_pos)
            self.grid.canvas.delete('food')
            self.grid.redraw_food()
            return True
        return False

    def pass_to_next_cycle(self):
        """Si la bacteria come, pasa al siguiente ciclo. Si no, termina la simulación."""
        self.num_cycles += 1
        if self.num_cycles >= self.max_cycles:  # Si ya alcanzó el máximo de ciclos, termina
            return False
        # Reiniciar el life_time para el siguiente ciclo
        self.life_time = 6
        self.initial_move = True
        self.last_position = None
        self.create_initial_point()
        return True
