from typing import List, Any
import os

class Player:
    def __init__(self, name: str, spots: List[int], mancala: int):
        self.name = name
        self.holes = spots
        self.mancala_spot: int = mancala

    def possible_holes(self) -> str:
        return ", ".join([str(x) for x in self.holes])

class Board:
    def __init__(self):
        self.board = self.create_board()
        self.player_a: Player = Player("A", [1, 2, 3, 4, 5, 6], 7)
        self.player_b: Player = Player("B", [8, 9, 10, 11, 12, 13], 0)
        self.current_player: Player = self.player_a

    @staticmethod
    def create_board() -> List[int]:
        created_board: List[int] = [4 for _ in range(14)]
        created_board[0] = 0
        created_board[7] = 0
        return created_board

    def is_valid_move(self, player: Player, position: int) -> bool:
        return True if position in player.holes and self.board[position] != 0 else False

    def make_move(self, position: int) -> None:
        beads: int = self.board[position]
        self.board[position] = 0
        index: int = position
        while beads > 0:
            index = (index + 1) % 14

            if index == self.get_opponent().mancala_spot:
                continue

            self.board[index] += 1
            beads -= 1

    def can_check_winner(self) -> bool:
        return True if sum(self.board[1:7]) == 0 or sum(self.board[8:]) == 0 else False

    def get_winner(self) -> Player:
        return self.player_a if sum(self.board[1:8]) > sum(self.board[8:]) + self.board[0] else self.player_b

    def tally_score(self) -> None:
        player_a_score: int = sum(self.board[1:8])
        player_b_score: int = sum(self.board[8:]) + self.board[0]

        self.board = [0 for _ in range(14)]
        self.board[7] = player_a_score
        self.board[0] = player_b_score


    def swap_players(self):
        self.current_player = self.get_opponent()

    def get_opponent(self) -> Player:
        return self.player_a if self.current_player == self.player_b else self.player_b

    def take_turn(self):
        print(f"Players {self.current_player.name}'s Turn!")
        print(f"Possible moves: {self.current_player.possible_holes()}")
        while True:
            try:
                move = int(input("Select a hole: "))
                if self.is_valid_move(self.current_player, move):
                    self.make_move(move)
                    self.swap_players()
                    break
                else:
                    print("Invalid move!")
            except ValueError:
                print("Invalid move!")


    def print_board(self):
        print(f"this {self.current_player.name}'s turn")
        print("\033[1;91m" + " " * 8 +self._format_row([x for x in range(13, 7, -1)]))
        print("-" * 8 * 7)
        print(self._format_row(["B:"] + self.board[14:7:-1]))
        print(f"{self.board[0]:^8}{' ' * 8 * 5}\033[1;94m{self.board[7]:^8}")
        print(self._format_row(["A:"] + self.board[1:7]))
        print("-" * 8 * 7)
        print(" " * 8 + self._format_row([x for x in range(1, 7)]) + "\033[0m")

    @staticmethod
    def _format_row(row: List[Any]) -> str:
        return "".join([f"{x:<8}" for x in row])

board = Board()

while True:
    os.system('clear')
    board.print_board()
    board.take_turn()
    if board.can_check_winner():
        board.tally_score()
        os.system('clear')
        board.print_board()
        print(f"Player {board.get_winner().name} wins!")
        break