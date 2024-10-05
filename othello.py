import pygame
import sys

class Orthello:
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 740
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Othello')
        
        self.rows = 8
        self.columns = 8
        self.cell_size = 80
        
        self.grid = Grid(self.rows, self.columns, self.cell_size, self)
        
        self.font = pygame.font.Font(None, 36)

        self.RUN = True

    def run(self):
        while self.RUN:
            self.input()
            self.update()
            self.draw()
            
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    x, y = pygame.mouse.get_pos()
                    col = (x // self.cell_size)
                    row = (y // self.cell_size) - 1  # Adjust for the player info height
                    
                    # Check if the move is valid
                    if self.grid.is_valid_move(row, col, self.grid.current_player):
                        self.grid.make_move(row, col, self.grid.current_player)
                        self.grid.switch_player()
                    else:
                        print("Invalid move!")

                # Check for pass turn condition
                if not self.grid.has_valid_moves(self.grid.current_player):
                    print(f"Player {'White' if self.grid.current_player == 1 else 'Black'} has no valid moves. Passing turn.")
                    self.grid.switch_player()

    def update(self):
        pass
    
    def draw(self):
        self.screen.fill((0, 128, 0))  # Fills screen with green for the board
        self.grid.drawGrid(self.screen)  # Draw the grid

        # Display current player and disk counts
        self.display_info()

        pygame.display.update()  # Update the display

    def display_info(self):
        white_count = self.grid.get_disk_count(1)
        black_count = self.grid.get_disk_count(-1)
        current_player_text = f"Current Player: {'White' if self.grid.current_player == 1 else 'Black'}"
        disk_count_text = f"White: {white_count} | Black: {black_count}"

        # Render the text
        current_player_surface = self.font.render(current_player_text, True, (255, 255, 255))
        disk_count_surface = self.font.render(disk_count_text, True, (255, 255, 255))

        # Blit the text onto the screen
        self.screen.blit(current_player_surface, (10, 10))
        self.screen.blit(disk_count_surface, (10, 50))

class Grid:
    def __init__(self, rows, columns, cell_size, main):
        self.GAME = main
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.gridLogic = self.regenGrid()
        self.current_player = 1  # 1 for white, -1 for black

    def regenGrid(self):
        grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        # Initialize the four center pieces
        grid[3][3] = 1  # White
        grid[3][4] = -1  # Black
        grid[4][3] = -1  # Black
        grid[4][4] = 1  # White
        return grid

    def drawGrid(self, window):
        # Draw the board
        for row in range(self.rows):
            for col in range(self.columns):
                # Draw the cell
                pygame.draw.rect(window, (0, 0, 0), (col * self.cell_size, row * self.cell_size + 80, self.cell_size, self.cell_size), 1)  # Draw grid lines

                # Draw tokens based on grid logic
                if self.gridLogic[row][col] == 1:  # White token
                    pygame.draw.circle(window, (255, 255, 255), (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2 + 80), self.cell_size // 2 - 5)
                elif self.gridLogic[row][col] == -1:  # Black token
                    pygame.draw.circle(window, (0, 0, 0), (col * self.cell_size + self.cell_size // 2, row * self.cell_size + self.cell_size // 2 + 80), self.cell_size // 2 - 5)

    def is_valid_move(self, row, col, player):
        if self.gridLogic[row][col] != 0:
            return False  # Cell is already occupied
        # Check if the move can flip any opponent's pieces
        opponent = -player
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.columns and self.gridLogic[r][c] == opponent:
                    while 0 <= r < self.rows and 0 <= c < self.columns:
                        if self.gridLogic[r][c] == player:
                            return True
                        if self.gridLogic[r][c] == 0:
                            break
                        r += dr
                        c += dc
        return False

    def make_move(self, row, col, player):
        self.gridLogic[row][col] = player  # Place the token
        opponent = -player
        # Flip opponent's pieces
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                to_flip = []
                while 0 <= r < self.rows and 0 <= c < self.columns:
                    if self.gridLogic[r][c] == opponent:
                        to_flip.append((r, c))
                    elif self.gridLogic[r][c] == player:
                        for flip in to_flip:
                            self.gridLogic[flip[0]][flip[1]] = player  # Flip pieces
                        break
                    else:
                        break
                    r += dr
                    c += dc

    def switch_player(self):
        self.current_player *= -1  # Switch between 1 and -1

    def get_disk_count(self, player):
        """Counts the number of disks for the specified player."""
        return sum(row.count(player) for row in self.gridLogic)

    def has_valid_moves(self, player):
        """Checks if the given player has any valid moves available."""
        for row in range(self.rows):
            for col in range(self.columns):
                if self.is_valid_move(row, col, player):
                    return True
        return False

if __name__ == '__main__':
    game = Orthello()
    game.run()
    pygame.quit()

