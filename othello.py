import pygame
import sys
# choose black/white player
# Make intitial game screen - add our names
# option to restart game
# potential move options
class Orthello:
    def __init__(self):
        # Initialize screen dimensions
        self.screen_width = 640
        self.screen_height = 740

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Othello')

        # Define game board parameters
        self.rows = 8
        self.columns = 8
        self.cell_size = 80

        # Create the grid for the game
        self.grid = Grid(self.rows, self.columns, self.cell_size, self)

        # Set up fonts for display text
        self.font = pygame.font.Font(None, 36)

        # Create an AI agent with depth level for minimax
        self.ai = MinimaxAgent(depth=3)

        # Define game state
        self.RUN = True
        self.valid_moves = []  # Initialize list of valid moves

    def title_screen(self):
        while True:
            self.screen.fill((0, 128, 0))  # Green background
            title_font = pygame.font.Font(None, 64)
            title_surface = title_font.render("Othello", True, (200, 200, 0))
            self.screen.blit(title_surface, (self.screen_width // 2 - title_surface.get_width() // 2, 100))
    
            # Button text surfaces
            play_white_surface = self.font.render("Play as White", True, (255, 255, 255))
            play_black_surface = self.font.render("Play as Black", True, (255, 255, 255))
    
            creators_surface = self.font.render("Created by Tyler Ton and Garrett Gmeiner", True, (255, 255, 255))
            self.screen.blit(creators_surface, (self.screen_width // 2 - creators_surface.get_width() // 2, 200))

            # Button positions
            white_button_rect = pygame.Rect(self.screen_width // 2 - play_white_surface.get_width() // 2 - 10, 
                                             300 - 10, 
                                             play_white_surface.get_width() + 20, 
                                             play_white_surface.get_height() + 20)
    
            black_button_rect = pygame.Rect(self.screen_width // 2 - play_black_surface.get_width() // 2 - 10, 
                                             350 - 10, 
                                             play_black_surface.get_width() + 20, 
                                             play_black_surface.get_height() + 20)
    
            # Draw button boxes
            pygame.draw.rect(self.screen, (255, 255, 255), white_button_rect, 2)  # White box
            pygame.draw.rect(self.screen, (255, 255, 255), black_button_rect, 2)  # Black box
    
            # Blit the button text
            self.screen.blit(play_white_surface, (self.screen_width // 2 - play_white_surface.get_width() // 2, 300))
            self.screen.blit(play_black_surface, (self.screen_width // 2 - play_black_surface.get_width() // 2, 350))
    
            pygame.display.update() # Updates board
    
            for event in pygame.event.get(): # Checks for quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print(f"Mouse clicked at: {x}, {y}")  # Debug print for mouse position
                    if white_button_rect.collidepoint(x, y):  # Check if "Play as White" button is clicked
                        print("Play as White clicked")  # Debug print
                        self.start_game(1)  # Player plays as White
                    elif black_button_rect.collidepoint(x, y):  # Check if "Play as Black" button is clicked
                        print("Play as Black clicked")  # Debug print
                        self.start_game(-1)  # Player plays as Black

    # Start the game with the chosen player color
    def start_game(self, player_color):
        self.grid.current_player = -1  # Set the current player based on choice
        #print("player_color", player_color, self.grid.current_player) #DEBUG
        self.run(player_color)  # Start the game loop

    # Main game loop
    def run(self, player_color):
        while self.RUN:
            self.input()       # Handle player input
            self.update(player_color)  # Update game state
            self.draw()        # Draw game elements
            
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False
                exit()

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

    def update(self, player_color):
        # Check if the board is full
        white_count = self.grid.get_disk_count(1)
        black_count = self.grid.get_disk_count(-1)
        if self.grid.is_board_full() or black_count == 0 or white_count == 0:
            # Determine the winner based on the counts
            if white_count > black_count:
                winner_text = "White wins!"
            elif black_count > white_count:
                winner_text = "Black wins!"
            else:
                winner_text = "It's a tie!"
            
            # Display the winner
            winner_surface = self.font.render(winner_text, True, (255, 255, 0))
            self.screen.blit(winner_surface, (self.screen_width // 2 - winner_surface.get_width() // 2, self.screen_height // 2))
            pygame.display.update()

            # Wait for a mouse click to quit
            waiting_for_click = True
            while waiting_for_click:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.RUN = False
                        waiting_for_click = False
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        waiting_for_click = False  # Exit the waiting loop
                        exit()
    
            self.RUN = False  # Ensure the game loop stops after the click

        # Check if it's the AI's turn and AI plays as white
        if self.grid.current_player == -1 and player_color == 1:
            ai_move = self.ai.choose_move(self.grid, self.grid.current_player)
            if ai_move is not None:
                self.grid.make_move(ai_move[0], ai_move[1], self.grid.current_player)
                self.grid.switch_player()
            else:
                print("AI has no valid moves.")
                self.grid.switch_player()
        # Check if it's the AI's turn and AI plays as black
        elif self.grid.current_player == 1 and player_color == -1:
            ai_move = self.ai.choose_move(self.grid, self.grid.current_player)
            if ai_move is not None:
                self.grid.make_move(ai_move[0], ai_move[1], self.grid.current_player)
                self.grid.switch_player()
            else:
                print("AI has no valid moves.")
                self.grid.switch_player()


    def draw(self):
        self.screen.fill((0, 128, 0))  # Fills screen with green for the board
        self.grid.drawGrid(self.screen)  # Draw the grid

        # Draw faint circles on valid moves
        for move in self.grid.get_all_valid_moves(self.grid.current_player):
            row, col = move
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2 + 80  # Adjust y for the header
            radius = self.cell_size * 0.2  # Circle radius (20% of cell size)
            pygame.draw.circle(self.screen, (0, 0, 255), (x, y), radius, 0)  # Faint blue circle

        # Display current player and disk counts
        self.display_info()

        pygame.display.update()  # Update the display

    # Display current player and disk counts on screen
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

class MinimaxAgent:
    # Set search depth and board position values for Minimax evaluation
    def __init__(self, depth):
        self.depth = depth
        
        self.position_value = [
            [100, -10, 10, 5, 5, 10, -10, 100],  # Emphasizing corners and edges
            [-10, -20, 0, 0, 0, 0, -20, -10],     # More weight for edges
            [10, 0, 1, 1, 1, 1, 0, 10],
            [5, 0, 1, 0, 0, 1, 0, 5],
            [5, 0, 0, 0, 0, 0, 0, 5],
            [10, 0, 1, 0, 0, 1, 0, 10],
            [-10, -20, 0, 0, 0, 0, -20, -10],
            [100, -10, 10, 5, 5, 10, -10, 100]   # Emphasizing corners and edges
        ]

    def evaluate_board(self, grid, player):
        """Evaluate the board state based on disc count, mobility, and position importance."""
        opponent = -player
        score = 0
        
        # Disc Count (Parity)
        player_count = grid.get_disk_count(player)
        opponent_count = grid.get_disk_count(opponent)
        score += player_count - opponent_count  # Favor player having more discs

        # Number of Legal Moves
        player_moves = len(grid.get_all_valid_moves(player))
        opponent_moves = len(grid.get_all_valid_moves(opponent))
        score += player_moves - opponent_moves  # Favor having more legal moves

        # Importance of Particular Positions
        for row in range(grid.rows):
            for col in range(grid.columns):
                if grid.gridLogic[row][col] == player:
                    score += self.position_value[row][col]
                elif grid.gridLogic[row][col] == opponent:
                    score -= self.position_value[row][col]

        # Additional strategic considerations
        score += self.corner_control(grid, player)  # Add score for corners
        score += self.edge_control(grid, player)    # Add score for edges

        return score

    def corner_control(self, grid, player):
        """Calculate score based on corner occupation."""
        opponent = -player
        corner_score = 0
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        
        for corner in corners:
            if grid.gridLogic[corner[0]][corner[1]] == player:
                corner_score += 50  # High value for occupying corners
            elif grid.gridLogic[corner[0]][corner[1]] == opponent:
                corner_score -= 50  # Deduct value for opponent's corner occupation

        return corner_score

    def edge_control(self, grid, player):
        """Calculate score based on edge occupation."""
        opponent = -player
        edge_score = 0
        edges = [(0, col) for col in range(8)] + [(7, col) for col in range(8)] + \
                [(row, 0) for row in range(1, 7)] + [(row, 7) for row in range(1, 7)]

        for edge in edges:
            if grid.gridLogic[edge[0]][edge[1]] == player:
                edge_score += 5  # Add points for occupying edges
            elif grid.gridLogic[edge[0]][edge[1]] == opponent:
                edge_score -= 5  # Deduct points for opponent's edge occupation

        return edge_score

    def minimax(self, grid, depth, maximizing_player, alpha=float('-inf'), beta=float('inf')):
        """The minimax algorithm with alpha-beta pruning."""
        if depth == 0 or grid.is_board_full():
            return self.evaluate_board(grid, maximizing_player), None

        valid_moves = grid.get_all_valid_moves(maximizing_player)

        if len(valid_moves) == 0:
            return self.evaluate_board(grid, maximizing_player), None
        if maximizing_player == 1:  # White's turn, maximizing player
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves: # Finds best move
                simulated_grid = grid.simulate_move(move[0], move[1], maximizing_player)
                evaluation = self.minimax(simulated_grid, depth - 1, -maximizing_player, alpha, beta)[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval, best_move
        else:  # Black's turn, minimizing player
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                simulated_grid = grid.simulate_move(move[0], move[1], maximizing_player)
                evaluation = self.minimax(simulated_grid, depth - 1, -maximizing_player, alpha, beta)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval, best_move

    def choose_move(self, grid, player):
        """Choose the best move for the player using minimax."""
        _, best_move = self.minimax(grid, self.depth, player)
        return best_move

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

    def is_board_full(self):
        """Checks if the board is full."""
        for row in self.gridLogic:
            if 0 in row:  # If there is an empty space, the board is not full
                return False
        return True
    
    def simulate_move(self, row, col, player):
        """Simulate a move and return a new grid with the move applied."""
        new_grid = Grid(self.rows, self.columns, self.cell_size, self.GAME)
        new_grid.gridLogic = [row.copy() for row in self.gridLogic]  # Deep copy of the grid
        new_grid.make_move(row, col, player)
        return new_grid

    def get_all_valid_moves(self, player):
        """Get all valid moves for the given player."""
        valid_moves = []
        for row in range(self.rows):
            for col in range(self.columns):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves


if __name__ == '__main__':
    game = Orthello()
    game.title_screen()
    pygame.quit()
