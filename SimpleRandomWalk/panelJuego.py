import tkinter as tk
from grid import Grid
from tkinter import simpledialog
from bacteria import Bacteria


class PanelJuego:
    def __init__(self, root, num_bacterias=3, num_food=10, life_time=20):
        self.root = root
        self.num_bacterias = num_bacterias
        self.num_food = num_food
        self.life_time = life_time
        self.ciclo_actual = 1  # Contador de ciclos, empezamos en 1
        self.setup_ui()
        self.grid.spawn_food(self.num_food)
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
        #self.bacteria = Bacteria(self.grid, self.update_cycle)

        # Crear las bacterias con identificadores únicos
        self.bacterias = [Bacteria(self.grid, self.update_cycle, bacteria_id=i, life_time=self.life_time) for i in range(self.num_bacterias)]




    def update_cycle(self, num_cycles):
        """Método para actualizar el ciclo en la interfaz"""
        self.ciclo_actual = num_cycles + 1
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.simulate_step()
        

    def simulate_step(self):
        print("\n--- Inicio de ciclo ---")
        if self.ciclo_actual > self.life_time:
            print("Simulación completada. Se alcanzó el máximo de pasos.")
            self.end_simulation()
            return
        alive_bacterias = [bacteria for bacteria in self.bacterias if bacteria.is_alive]
        if not alive_bacterias:
            print("Todas las bacterias murieron. Simulación finalizada.")
            self.end_simulation()
            return
        for bacteria in alive_bacterias:
            bacteria.move()
        self.ciclo_actual += 1
        print(f"Ciclo: {self.ciclo_actual}, Bacterias vivas: {[b.bacteria_id for b in alive_bacterias]}")
        self.simulation_timer = self.root.after(1000, self.simulate_step)

    def end_simulation(self):
        """Finaliza la simulación"""
        self.grid.canvas.delete('bacteria')
        print("Simulación finalizada. Todas las bacterias han muerto.")

       # Actualizar el ciclo actual en el label
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

    def restart_game(self):
        """Reiniciar el juego"""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)
        # Limpiar la cuadrícula y reiniciar las bacterias
        self.grid.create_grid()
        self.bacterias = [Bacteria(self.grid, self.update_cycle, bacteria_id=i, life_time=self.life_time) for i in range(self.num_bacterias)]


        # Restablecer el ciclo a 1
        self.ciclo_actual = 1
        self.ciclo_label.config(text=f"Ciclo: {self.ciclo_actual}")

        # Volver a generar comida inicial y reiniciar la simulación
        self.grid.spawn_food(self.num_food)
        self.start_simulation()

if __name__ == "__main__":
    root = tk.Tk()
    num_food = simpledialog.askinteger("Configuración", "Ingrese el número de comidas:", minvalue=1, maxvalue=100)
    life_time = simpledialog.askinteger("Configuración", "Ingrese el tiempo de vida de las bacterias:", minvalue=1, maxvalue=100)
    
    if num_food and life_time:
        app = PanelJuego(root, num_bacterias=3, num_food=num_food, life_time=life_time)
        root.mainloop()