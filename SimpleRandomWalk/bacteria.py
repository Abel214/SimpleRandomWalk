from random import choice

class Bacteria:
    def __init__(self, grid):
        self.grid = grid
        self.canvas = grid.canvas
        self.cell_size = grid.cell_size
        self.grid_size = grid.size
        self.life_time = 5  # Tiempo de vida
        self.create_initial_point()

    def create_initial_point(self):
        """Create point in a random corner"""
        # Define corners (grid coordinates)
        corners = [
            (0, 0),  # Top left
            (0, self.grid_size - 1),  # Bottom left
            (self.grid_size - 1, 0),  # Top right
            (self.grid_size - 1, self.grid_size - 1)  # Bottom right
        ]

        # Choose random corner
        self.grid_x, self.grid_y = choice(corners)
        self.draw_point()

    def draw_point(self):
        """Draw point at current position"""
        pixel_x = self.grid_x * self.cell_size
        pixel_y = self.grid_y * self.cell_size

        # Delete previous point if exists
        self.canvas.delete('point')

        # Draw new point
        padding = self.cell_size // 4
        self.canvas.create_oval(
            pixel_x + padding,
            pixel_y + padding,
            pixel_x + self.cell_size - padding,
            pixel_y + self.cell_size - padding,
            fill='green',
            tag='point'
        )

    def move(self):
        """Move the bacteria randomly and return whether it's still alive"""
        if self.life_time <= 0:
            return False

        # Possible movements in grid coordinates (up, down, left, right)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        move = choice(directions)

        # Calculate new position
        new_x = self.grid_x + move[0]
        new_y = self.grid_y + move[1]

        # Check if movement is within grid boundaries
        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            self.grid_x = new_x
            self.grid_y = new_y

            # Check if there's food at new position
            if self.check_food_collision():
                self.life_time += 5  # Increase lifetime when eating
                self.grid.spawn_food()  # Respawn food

            self.draw_point()

        self.life_time -= 1
        return True

    def check_food_collision(self):
        """Check if bacteria collides with food at current position"""
        current_pos = (self.grid_x, self.grid_y)
        if current_pos in self.grid.food_positions:
            self.grid.food_positions.remove(current_pos)
            return True
        return False

    def get_lifetime(self):
        """Return current lifetime"""
        return self.life_time