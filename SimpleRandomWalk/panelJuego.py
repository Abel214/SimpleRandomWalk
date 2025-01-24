import tkinter as tk
from bacteria import Bacteria
from grid import Grid

MAX_CYCLES = 6

class PanelJuego:
    def __init__(self, root, num_bacterias=2, num_food=50, steps_per_bacteria=6):
        self.root = root
        self.num_bacterias = num_bacterias
        self.num_food = num_food
        self.steps_per_bacteria = steps_per_bacteria
        self.current_cycle = 1
        self.setup_ui()
        self.grid.spawn_initial_food(self.num_food)  # Generar comida inicial
        self.simulation_timer = None
        self.start_simulation()

    def setup_ui(self):
        """Configurar la interfaz del juego"""
        # Panel principal
        self.panel = tk.Frame(
            self.root,
            bg='gray10',
            padx=20,
            pady=20
        )
        self.panel.pack(expand=True, fill='both')

        # Panel superior para controles futuros
        self.control_panel = tk.Frame(
            self.panel,
            bg='gray10'
        )
        self.control_panel.pack(fill='x', pady=(0, 10))
        self.repeat_button = tk.Button(
            self.control_panel,
            text="Repetir",
            command=self.restart_game,
            bg='gray30',
            fg='white',
            font=("Arial", 12),
            relief="raised"
        )
        self.cycle_label = tk.Label(
            self.control_panel,
            text=f"Ciclo: {self.current_cycle}",
            bg='gray10',
            fg='white',
            font=("Arial", 12)
        )
        self.cycle_label.pack(side="left", padx=10)
        self.repeat_button.pack(side="left", padx=10)

        # Panel para la grid
        self.game_frame = tk.Frame(
            self.panel,
            bg='gray10'
        )
        self.game_frame.pack(expand=True)

        # Crear la grid dentro del panel de juego
        self.grid = Grid(self.game_frame)

        # Crear las bacterias con identificadores únicos
        self.bacterias = [
            Bacteria(self.grid, i, self.steps_per_bacteria)
            for i in range(self.num_bacterias)
        ]  # Crear bacterias con el número de pasos

    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.grid.spawn_initial_food(self.num_food)  # Generar las comidas iniciales
        self.simulate_step()

    def simulate_step(self):
        """Simular un paso de movimiento de las bacterias."""
        print(f"\n--- Ciclo {self.current_cycle} ---")
        self.cycle_label.config(text=f"Ciclo: {self.current_cycle}")

        # Eliminar bacterias muertas del panel
        for bacteria in self.bacterias:
            if not bacteria.is_alive:
                self.grid.canvas.delete(f'bacteria_{bacteria.bacteria_id}')
                self.grid.canvas.delete(f'bacteria_{bacteria.bacteria_id}_text')

        # Actualizar el estado de todas las bacterias
        all_waiting = True
        for bacteria in self.bacterias:
            if bacteria.is_alive:
                if not bacteria.waiting_for_others:  # Si la bacteria no está esperando, que se mueva
                    all_waiting = False
                    if not bacteria.move():  # Si la bacteria muere durante el movimiento
                        bacteria.canvas.delete(f'bacteria_{bacteria.bacteria_id}')
                else:
                    print(f"Bacteria {bacteria.bacteria_id} está esperando a que termine el ciclo")

        # Verificar cuántas bacterias están vivas
        alive_bacterias = [bacteria for bacteria in self.bacterias if bacteria.is_alive]

        if not alive_bacterias:
            self.end_simulation()
            return

        # Si todas las bacterias vivas están esperando, iniciar nuevo ciclo
        if all_waiting:
            for bacteria in alive_bacterias:
                bacteria.waiting_for_others = False  # Resetear el estado de espera
            self.start_new_cycle(alive_bacterias)
        else:
            # Continuar con el siguiente paso en el ciclo actual
            print(f"Bacterias vivas en ciclo {self.current_cycle}: {[b.bacteria_id for b in alive_bacterias]}")
            self.simulation_timer = self.root.after(1000, self.simulate_step)

    def start_new_cycle(self, alive_bacterias):
        """Iniciar un nuevo ciclo de la simulación sin regenerar comida."""
        if self.current_cycle >= MAX_CYCLES:
            print("Se ha alcanzado el número máximo de ciclos. Simulación finalizada.")
            self.end_simulation()
            return

        self.current_cycle += 1
        print(f"\n=== Iniciando Ciclo {self.current_cycle} ===")

        # Filtrar bacterias vivas para el siguiente ciclo
        surviving_bacteria = []
        for bacteria in alive_bacterias:
            # Si la bacteria tiene vida 1 y ha comido, no se elimina
            if bacteria.life_time > 1 or (bacteria.life_time == 1 and bacteria.has_eaten):
                if bacteria.pass_to_next_cycle():  # Verifica si la bacteria puede pasar al siguiente ciclo
                    surviving_bacteria.append(bacteria)
                    print(f"Bacteria {bacteria.bacteria_id} inicia ciclo {self.current_cycle}")
                else:
                    print(f"Bacteria {bacteria.bacteria_id} no sobrevive al siguiente ciclo. Eliminada.")
                    self.grid.canvas.delete(f'bacteria_{bacteria.bacteria_id}')
                    self.grid.canvas.delete(f'bacteria_{bacteria.bacteria_id}_text')

        if surviving_bacteria:
            print(f"Bacterias que pasan al ciclo {self.current_cycle}: {[b.bacteria_id for b in surviving_bacteria]}")
            self.simulation_timer = self.root.after(1000, self.simulate_step)
        else:
            print("Ninguna bacteria sobrevivió al nuevo ciclo. Simulación finalizada.")
            self.end_simulation()

    def end_simulation(self):
        """Finaliza la simulación y muestra cuántos ciclos faltaron."""
        # Calcular cuántos ciclos faltaron
        cycles_remaining = MAX_CYCLES - self.current_cycle

        # Eliminar las bacterias del panel
        self.grid.canvas.delete('bacteria')

        # Mostrar el mensaje de finalización
        if cycles_remaining > 0:
            print(f"Simulación finalizada. Todas las bacterias han muerto. Faltaron {cycles_remaining} ciclos.")
        else:
            print("Simulación finalizada. Todas las bacterias han muerto.")

    def restart_game(self):
        """Reiniciar el juego"""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)
        self.current_cycle = 1
        # Limpiar la cuadrícula y reiniciar las bacterias
        self.grid.create_grid()
        self.bacterias = [
            Bacteria(self.grid, i, self.steps_per_bacteria)
            for i in range(self.num_bacterias)
        ]  # Crear bacterias con el número de pasos

        # Volver a generar comida inicial y reiniciar la simulación
        self.grid.spawn_initial_food(self.num_food)  # Asegurarse de que se generen correctamente las comidas
        self.start_simulation()

root = tk.Tk()
root.title("Simple Random Walk")
# Establecer el tamaño de la ventana
root.geometry()

# Centrar la ventana en la pantalla
position_top = 50
position_right = 500

root.geometry(f"700x600+{position_right}+{position_top}")
# Iniciar la aplicación
app = PanelJuego(root)
root.mainloop()
