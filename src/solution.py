from player import Player
from board import HexBoard
import heapq
import time

class SmartPlayer(Player):
    
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.opp = 2 if player_id == 1 else 1
        self.depth = 2
        self.trans_table = {}  # transposition table
    
    
    def play(self, board: HexBoard) -> tuple:
        pass
        
    
 
    def _order_moves(self, board, moves, player):
        """
        Ordena movimientos de mejor a peor según heurística rápida.
        Para MAX: queremos minimizar dijkstra(self) → menor es mejor.
        Para MIN: queremos minimizar dijkstra(opp)  → menor es mejor para el oponente.
        """
        def score(move):
            r, c = move
            board.board[r][c] = player               # make temporal
            # heurística: diferencia de distancias tras el movimiento
            s = self._eval(board)
            board.board[r][c] = 0                    # unmake
            return s

        # MAX quiere score alto, MIN quiere score bajo
        reverse = (player == self.player_id)
        return sorted(moves, key=score, reverse=reverse)

    
    def _get_relevant_moves(self, board):
        """Solo celdas adyacentes a piezas ya jugadas."""
        candidates = set()
        for r in range(board.size):
            for c in range(board.size):
                if board.board[r][c] != 0:
                    for nr, nc in board._get_neighbors(r, c):
                        if board.board[nr][nc] == 0:
                            candidates.add((nr, nc))
        if not candidates:
            return [(r, c) for r in range(board.size)
                    for c in range(board.size) if board.board[r][c] == 0]
        return list(candidates)
    
    
    
    def _terminal(self, board):
        return board.check_connection(self.player_id) or \
               board.check_connection(self.opp)

    
    def _board_hash(self, board):
        """Hash compacto del estado del tablero."""
        return tuple(board.board[r][c]
                     for r in range(board.size)
                     for c in range(board.size))
    
    
    
    def _eval(self, board):
        return self._dijkstra(board, self.opp) - self._dijkstra(board, self.player_id)
    
    
    def _dijkstra(self, b, p):
        pq = []
        visited = {}
        for i in range(b.size):
            r, c = (i, 0) if p == 1 else (0, i)
            w = 0 if b.board[r][c] == p else (1 if b.board[r][c] == 0 else float('inf'))
            if w < float('inf'):
                heapq.heappush(pq, (w, r, c))
        while pq:
            d, r, c = heapq.heappop(pq)
            if (r, c) in visited:
                continue
            visited[(r, c)] = d
            if (p == 1 and c == b.size - 1) or (p == 2 and r == b.size - 1):
                return d
            for nr, nc in b._get_neighbors(r, c):
                if (nr, nc) not in visited:
                    w = 0 if b.board[nr][nc] == p else (1 if b.board[nr][nc] == 0 else float('inf'))
                    if w < float('inf'):
                        heapq.heappush(pq, (d + w, nr, nc))
        return float('inf')