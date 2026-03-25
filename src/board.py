
class HexBoard:
    def __init__(self, size: int):
        self.size = size # Tamaño N del tablero (NxN)
        self.board = [[0 for _ in range(size)] for _ in range(size)] 
        #Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
    
    def clone(self) :
        """Devuelve una copia del tablero actual"""
        new_board = HexBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        return new_board
    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """Coloca una ficha si la casilla está vacía."""
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == 0:
            self.board[row][col] = player_id
            return True
        return False
    
    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados"""
        size = self.size
        visited = set()
        # Jugador 1: Izquierda (col 0) a Derecha (col N-1)
        # Jugador 2: Superior (fila 0) a Inferior (fila N-1)
        
        start_nodes = []
        for i in range(size):
            if player_id == 1 and self.board[i][0] == player_id:
                start_nodes.append((i, 0))
            elif player_id == 2 and self.board[0][i] == player_id:
                start_nodes.append((0, i))

        stack = start_nodes
        while stack:
            r, c = stack.pop()
            if (r, c) in visited: continue
            visited.add((r, c))

            if (player_id == 1 and c == size - 1) or (player_id == 2 and r == size - 1):
                return True

            for nr, nc in self._get_neighbors(r, c):
                if self.board[nr][nc] == player_id:
                    stack.append((nr, nc))
        return False
    
    def _get_neighbors(self, r, c):
        """Implementación de adyacencias even-r layout """
        res = []
        potential = [(r, c-1), (r, c+1)]
        if r % 2 == 0:
            potential += [(r-1, c-1), (r-1, c), (r+1, c-1), (r+1, c)]
        else:
            potential += [(r-1, c), (r-1, c+1), (r+1, c), (r+1, c+1)]
        for nr, nc in potential:
            if 0 <= nr < self.size and 0 <= nc < self.size:
                res.append((nr, nc))
        return res