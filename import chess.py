import tkinter as tk
import chess
# Constants used  for the chessboard
BOARD_SIZE = 8
SQUARE_SIZE = 60
LIGHT_COLOR = "#F0D9B5"
DARK_COLOR = "#B58863"
HIGHLIGHT_COLOR = "#FFD700"
MOVE_MARKER_COLOR = "#87CEEB"
# Piece symbols which is used in the chessboard 
PIECE_SYMBOLS = {
    'P': "♙", 'p': "♟",
    'R': "♖", 'r': "♜",
    'N': "♘", 'n': "♞",
    'B': "♗", 'b': "♝",
    'Q': "♕", 'q': "♛",
    'K': "♔", 'k': "♚",
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
        self.draw_board()
        self.draw_pieces()
        # Bind mouse click to handle moves
        self.canvas.bind("<Button-1>", self.on_click)
    def draw_board(self):
        #Draw the chessboard with optional highlighting.
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
        """Draw the chess pieces on the board."""
        for square, piece in self.board.piece_map().items():
            row, col = divmod(square, BOARD_SIZE)
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = (BOARD_SIZE - 1 - row) * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=PIECE_SYMBOLS[str(piece)], font=("Arial", SQUARE_SIZE // 2))
    def on_click(self, event):
        #Handle mouse click to move pieces.
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
            self.selected_square = None
            self.legal_moves = []

        self.draw_board()
        self.draw_pieces()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
