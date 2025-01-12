import tkinter as tk
from SimpleRandomWalk.bacteria import Bacteria
from grid import Grid


class PanelJuego:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.grid.spawn_food()  # Generar comida inicial
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

        # Panel para la grid
        self.game_frame = tk.Frame(
            self.panel,
            bg='gray10'
        )
        self.game_frame.pack(expand=True)

        # Crear la grid dentro del panel de juego
        self.grid = Grid(self.game_frame)
        self.bacteria = Bacteria(self.grid)

    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.simulate_step()

    def simulate_step(self):
        """Simular un paso de movimiento de la bacteria"""
        is_alive = self.bacteria.move()

        # Si la bacteria sigue viva, llama a simulate_step después de 500 ms
        if is_alive:
            self.root.after(500, self.simulate_step)
        else:
            print("La bacteria ha muerto.")


root = tk.Tk()
app = PanelJuego(root)
root.mainloop()
