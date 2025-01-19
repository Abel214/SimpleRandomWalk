import tkinter as tk
from grid import Grid
from bacteria import Bacteria


class PanelJuego:
    def __init__(self, root):
        self.root = root
        self.ciclo_actual = 1  # Contador de ciclos, empezamos en 1
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
        
        # Etiqueta para mostrar el ciclo actual
        self.ciclo_label = tk.Label(
            self.control_panel,
            text=f"Ciclo: {self.ciclo_actual}",
            bg='gray10',
            fg='white',
            font=("Arial", 12)
        )
        self.ciclo_label.pack(side="left", padx=10)

        # Botón de repetir
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
        self.bacteria = Bacteria(self.grid, self.update_cycle)

    def update_cycle(self, num_cycles):
        """Método para actualizar el ciclo en la interfaz"""
        self.ciclo_actual = num_cycles + 1
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.grid.spawn_initial_food(10)  # Generar las 10 comidas iniciales
        self.simulate_step()
        

    def simulate_step(self):
        """Simular un paso de movimiento de la bacteria"""
        is_alive = self.bacteria.move()

        # Si la bacteria sigue viva, llama a simulate_step después de 500 ms
        if is_alive:
            # Si ya hay un temporizador activo, cancelarlo
            if self.simulation_timer is not None:
                self.root.after_cancel(self.simulation_timer)
            # Programar el siguiente paso
            self.simulation_timer = self.root.after(1000, self.simulate_step)
        else:
            print(f"Simulación completada. Ciclos terminados: {self.bacteria.num_cycles}")
            self.end_simulation()

    def end_simulation(self):
        """Finaliza la simulación"""
        self.grid.canvas.delete('bacteria')
        print("Fin de la simulación.")

       # Actualizar el ciclo actual en el label
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

    def restart_game(self):
        """Reiniciar el juego"""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)
        # Limpiar la cuadrícula y reiniciar la bacteria
        self.grid.create_grid()
        self.bacteria = Bacteria(self.grid, self.update_cycle)

        # Restablecer el ciclo a 1
        self.ciclo_actual = 1
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

        # Volver a generar comida inicial y reiniciar la simulación
        self.grid.spawn_food()
        self.start_simulation()

root = tk.Tk()
app = PanelJuego(root)
root.mainloop()
