import tkinter as tk
from SimpleRandomWalk.bacteria import Bacteria
from grid import Grid


class PanelJuego:
    def __init__(self, root, num_bacterias=7):
        self.root = root
        self.num_bacterias = num_bacterias
        self.setup_ui()
        self.grid.spawn_food()  # Generar comida inicial
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
        self.bacterias = [Bacteria(self.grid, bacteria_id=i) for i in range(self.num_bacterias)]



    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.grid.spawn_initial_food(10)  # Generar las 10 comidas iniciales
        self.simulate_step()

    def simulate_step(self):
        """Simular un paso de movimiento de las bacterias."""
        print("\n--- Inicio de ciclo ---")
        # Actualizar el estado de todas las bacterias
        for bacteria in self.bacterias:
            bacteria.move()

        # Verificar cuántas bacterias están vivas
        alive_bacterias = [bacteria for bacteria in self.bacterias if bacteria.is_alive]

        if not alive_bacterias:  # Si no quedan bacterias vivas
            print("Todas las bacterias murieron. Simulación finalizada.")
            self.end_simulation()
            return

        # Continuar con el siguiente ciclo
        print(f"Bacterias vivas: {[b.bacteria_id for b in alive_bacterias]}")
        self.simulation_timer = self.root.after(1000, self.simulate_step)

    def end_simulation(self):
        """Finaliza la simulación"""
        self.grid.canvas.delete('bacteria')
        print("Simulación finalizada. Todas las bacterias han muerto.")

    def restart_game(self):
        """Reiniciar el juego"""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)
        # Limpiar la cuadrícula y reiniciar las bacterias
        self.grid.create_grid()
        self.bacterias = [Bacteria(self.grid, bacteria_id=i) for i in range(self.num_bacterias)]

        # Volver a generar comida inicial y reiniciar la simulación
        self.grid.spawn_food()
        self.start_simulation()

root = tk.Tk()
app = PanelJuego(root)
root.mainloop()
