import tkinter as tk
import chess
import time

# Constants used for the chessboard
BOARD_SIZE = 8
SQUARE_SIZE = 60
LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#FFD700"
MOVE_MARKER_COLOR = "#87CEEB"

# Piece symbols used in the chessboard
Piece_symbol = {
    'P': "\u2659", 'p': "\u265F",
    'R': "\u2656", 'r': "\u265C",
    'N': "\u2658", 'n': "\u265E",
    'B': "\u2657", 'b': "\u265D",
    'Q': "\u2655", 'q': "\u265B",
    'K': "\u2654", 'k': "\u265A",
}

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Visualizer")
        self.board = chess.Board()

        # Create a canvas for the chessboard
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
        self.canvas.pack()

        self.selected_square = None
        self.legal_moves = []
        self.turn_timer = 30  # 30 seconds per turn
        self.timer_running = False

        self.draw_board()
        self.draw_pieces()

        # Bind mouse click to handle moves
        self.canvas.bind("<Button-1>", self.on_click)

        # Add control buttons
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.start_button = tk.Button(self.controls_frame, text="Start New Game", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.restart_button = tk.Button(self.controls_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.controls_frame, text="Exit Game", command=self.exit_game)
        self.exit_button.pack(side=tk.LEFT, padx=10)

        # Timer display
        self.timer_label = tk.Label(self.controls_frame, text=f"Time Left: {self.turn_timer}s", font=("Arial", 14))
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # Start the timer
        self.start_timer()

    def start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.turn_timer > 0:
            self.turn_timer -= 1
            self.timer_label.config(text=f"Time Left: {self.turn_timer}s")
            self.root.after(1000, self.update_timer)
        else:
            self.end_turn()

    def end_turn(self):
        # Switch turn to the other player
        self.turn_timer = 30  # Reset timer to 30 seconds
        self.draw_board()
        self.draw_pieces()

    def draw_board(self):
        # Draw the chessboard with optional highlighting.
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                square = chess.square(col, BOARD_SIZE - 1 - row)

                # Highlight selected square
                if self.selected_square == square:
                    color = HIGHLIGHT_COLOR

                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        # Draw move markers
        for move in self.legal_moves:
            to_square = move.to_square
            col = chess.square_file(to_square)
            row = BOARD_SIZE - 1 - chess.square_rank(to_square)
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            self.canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=MOVE_MARKER_COLOR, outline="")

    def draw_pieces(self):
        # Draw the chess pieces on the board.
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, BOARD_SIZE)
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = (BOARD_SIZE - 1 - row) * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=Piece_symbol[str(piece)], font=("Arial", SQUARE_SIZE // 2))

    def on_click(self, event):
        # Handle mouse click to move pieces.
        col = event.x // SQUARE_SIZE
        row = BOARD_SIZE - 1 - (event.y // SQUARE_SIZE)
        clicked_square = chess.square(col, row)

        if self.selected_square is None:
            # First click: select a piece
            if self.board.piece_at(clicked_square):
                self.selected_square = clicked_square
                self.legal_moves = [move for move in self.board.legal_moves if move.from_square == self.selected_square]
        else:
            # Second click: make a move
            move = chess.Move(self.selected_square, clicked_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.end_turn()  # End the current player's turn after a valid move
            self.selected_square = None
            self.legal_moves = []

        self.draw_board()
        self.draw_pieces()

    def start_game(self):
        # Start a new game
        self.board = chess.Board()
        self.selected_square = None
        self.legal_moves = []
        self.turn_timer = 30  # Reset timer
        self.draw_board()
        self.draw_pieces()
        self.start_timer()

    def restart_game(self):
        # Restart the current game
        self.board.reset()
        self.selected_square = None
        self.legal_moves = []
        self.turn_timer = 30  # Reset timer
        self.draw_board()
        self.draw_pieces()
        self.start_timer()

    def exit_game(self):
        # Exit the application
        self.root.destroy()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
