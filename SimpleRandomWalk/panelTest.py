import tkinter as tk
from bacteria import Bacteria
from tkinter import ttk  # Para el ComboBox
from gridTest import Grid

MAX_CYCLES = 6

class PanelJuego:
    def __init__(self, root, num_bacterias=2, num_food=50, steps_per_bacteria=6):
        self.root = root
        self.num_bacterias = num_bacterias
        self.num_food = num_food
        self.steps_per_bacteria = steps_per_bacteria
        self.current_cycle = 1
        self.message_label = None
        self.simulation_timer = None
        self.biome = None
        self.is_simulating = False  # Variable para controlar el estado de simulación
        
        self.setup_ui()
        self.create_grid()
        self.grid.spawn_initial_food(self.num_food)
        self.start_simulation()

    def setup_ui(self):
        """Configurar la interfaz del juego."""
        self.panel = tk.Frame(self.root, bg='gray10', padx=20, pady=20)
        self.panel.pack(expand=True, fill='both')

        self.control_panel = tk.Frame(self.panel, bg='gray10')
        self.control_panel.pack(fill='x', pady=(0, 10))

        self.repeat_button = tk.Button(
            self.control_panel, text="Iniciar", command=self.restart_game,
            bg='gray30', fg='white', font=("Arial", 12), relief="raised"
        )
        self.repeat_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(
            self.control_panel, text="Terminar", command=self.detener_simulacion,
            bg='gray30', fg='white', font=("Arial", 12), relief="raised"
        )
        self.stop_button.pack(side="left", padx=10)

        self.cycle_label = tk.Label(
            self.control_panel, text=f"Ciclo: {self.current_cycle}",
            bg='gray10', fg='white', font=("Arial", 12)
        )
        self.cycle_label.pack(side="left", padx=10)

        self.biome_label = tk.Label(
            self.control_panel, text="Seleccionar Bioma:", bg='gray10', fg='white'
        )
        self.biome_label.pack(side="left", padx=10)

        self.biome_combo = ttk.Combobox(
            self.control_panel, values=["Ninguno", "invierno", "verano"], state="readonly"
        )
        
        self.biome_combo.current(0)
        self.biome_combo.pack(side="left", padx=10)
        self.biome_combo.bind("<<ComboboxSelected>>", self.change_biome)

        self.game_frame = tk.Frame(self.panel, bg='gray10')
        self.game_frame.pack(expand=True)

    def create_grid(self):
        """Crear o actualizar la grid con el bioma seleccionado."""
        if hasattr(self, 'grid'):
            self.grid.canvas.destroy()
        self.grid = Grid(self.game_frame, biome=self.biome)
        self.bacterias = [Bacteria(self.grid, i, self.steps_per_bacteria) for i in range(self.num_bacterias)]

    def change_biome(self, event):
        """Actualizar la grid cuando cambia el bioma."""
        if self.is_simulating:
            return  # No hacer nada si la simulación está en curso
        
        self.biome = self.biome_combo.get()
        self.create_grid()


    def start_simulation(self):
        """Iniciar la simulación del movimiento"""
        self.is_simulating = True
        self.biome_combo.config(state="disabled")

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

        # Determinar el mensaje de finalización
        if cycles_remaining > 0:
            message = f"Simulación finalizada.\n Todas las bacterias han muerto.\n Faltaron {cycles_remaining} ciclos."
        else:
            message = "Simulación finalizada.\n Todas las bacterias han muerto."

        # Eliminar el mensaje anterior si existe
        if self.message_label is not None:
            self.message_label.destroy()

        # Crear un nuevo widget Label para mostrar el mensaje
        self.message_label = tk.Label(self.grid.canvas, text=message, font=("Arial", 14), fg="red")
        self.message_label.place(relx=0.5, rely=0.5, anchor="center")  # Ubicarlo en el centro del canvas

        self.is_simulating = False
        self.biome_combo.config(state="readonly")

    def detener_simulacion(self):
        """Detener todo el ciclo y las bacterias."""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)

        self.is_simulating = False
        self.biome_combo.config(state="readonly")

        # Eliminar bacterias del panel
        self.grid.canvas.delete('all')

        # Eliminar el mensaje anterior si existe
        if self.message_label is not None:
            self.message_label.destroy()
            self.message_label = None

        # Crear un nuevo widget Label para mostrar el mensaje
        self.message_label = tk.Label(self.grid.canvas, text="Simulación detenida.", font=("Arial", 14), fg="red")
        self.message_label.place(relx=0.5, rely=0.5, anchor="center")  # Ubicarlo en el centro del canvas

    def restart_game(self):
        """Reiniciar el juego"""
        if self.simulation_timer is not None:
            self.root.after_cancel(self.simulation_timer)

        # Reiniciar ciclo actual
        self.current_cycle = 1

        # Limpiar la cuadrícula y eliminar el mensaje
        if self.message_label is not None:
            self.message_label.destroy()  # Eliminar el mensaje de finalización
            self.message_label = None

        # Reiniciar la cuadrícula y las bacterias
        self.grid.create_grid()
        self.bacterias = [
            Bacteria(self.grid, i, self.steps_per_bacteria)
            for i in range(self.num_bacterias)
        ]

        # Volver a generar comida inicial y reiniciar la simulación
        self.grid.spawn_initial_food(self.num_food)
        self.start_simulation()

    def abrir_ventana(self):
        """Abre una nueva ventana para ejecutar la clase desde otra clase."""
        new_window = tk.Toplevel(self.root)
        # Get the screen dimensions
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()

        # Set the window dimensions
        window_width = 800  # You can adjust the size as needed
        window_height = 600  # You can adjust the size as needed

        # Calculate the position to center the window
        position_x = int((screen_width / 2) - (window_width / 2))
        position_y = int((screen_height / 2) - (window_height / 2))

        # Set the geometry of the window
        new_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Initialize the PanelJuego in the new window
        PanelJuego(new_window, self.num_bacterias, self.num_food, self.steps_per_bacteria)
        

