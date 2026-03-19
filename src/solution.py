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
        
    
    def _root_search(self, board, start):
        best_val = float('-inf')
        best_move = None
        alpha, beta = float('-inf'), float('inf')

        # ── Move Ordering en la raíz ─────────
        moves = self._get_relevant_moves(board)
        ordered = self._order_moves(board, moves, self.player_id)

        for r, c in ordered:
            if time.time() - start > 4.0:
                break
            board.board[r][c] = self.player_id          
            val = self._min_v(board, 1, alpha, beta)
            board.board[r][c] = 0                        
            if val > best_val:
                best_val, best_move = val, (r, c)
            alpha = max(alpha, best_val)

        return best_val, best_move
    
    
    def _max_v(self, board, d, a, b):
        # ── Transposition Table lookup ───────
        key = (self._board_hash(board), d, 'max')
        if key in self.trans_table:
            return self.trans_table[key]

        if d == self.depth or self._terminal(board):
            return self._eval(board)

        v = float('-inf')
        for r, c in self._order_moves(board, self._get_relevant_moves(board), self.player_id):
            board.board[r][c] = self.player_id           
            v = max(v, self._min_v(board, d + 1, a, b))
            board.board[r][c] = 0                        
            if v >= b:
                self.trans_table[key] = v
                return v
            a = max(a, v)

        self.trans_table[key] = v
        return v

    def _min_v(self, board, d, a, b):
        # ── Transposition Table lookup ───────
        key = (self._board_hash(board), d, 'min')
        if key in self.trans_table:
            return self.trans_table[key]

        if d == self.depth or self._terminal(board):
            return self._eval(board)

        v = float('inf')
        for r, c in self._order_moves(board, self._get_relevant_moves(board), self.opp):
            board.board[r][c] = self.opp                 
            v = min(v, self._max_v(board, d + 1, a, b))
            board.board[r][c] = 0                        
            if v <= a:
                self.trans_table[key] = v
                return v
            b = min(b, v)

        self.trans_table[key] = v
        return v
    
    
    def _order_moves(self, board, moves, player):
        """
        Ordena movimientos de mejor a peor según heurística rápida.
        Para MAX: queremos minimizar dijkstra(self) → menor es mejor.
        Para MIN: queremos minimizar dijkstra(opp)  → menor es mejor para el oponente.
        """
        def score(move):
            r, c = move
            board.board[r][c] = player               
            # heurística: diferencia de distancias tras el movimiento
            s = self._eval(board)
            board.board[r][c] = 0                    
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