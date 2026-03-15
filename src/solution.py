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