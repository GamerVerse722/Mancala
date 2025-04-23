from typing import List, Any, Optional
import os

class Player:
    def __init__(self, name: str, spots: List[int], mancala: int):
        self.name = name
        self.holes = spots
        self.mancala_spot: int = mancala

    def possible_holes(self) -> str:
        return ", ".join([str(x) for x in self.holes])

class Board:
    def __init__(self) -> None:
        self.board = self.create_board()
        self.player_a: Player = Player("A", [1, 2, 3, 4, 5, 6], 7)
        self.player_b: Player = Player("B", [13, 12, 11, 10, 9, 8], 0)
        self.current_player: Player = self.player_a
        self._last_captured: bool = False
        self.was_captured: bool = False
        self.landed_on_mancala: bool = False

    @staticmethod
    def create_board() -> List[int]:
        created_board: List[int] = [4 for _ in range(14)]
        created_board[0] = 0
        created_board[7] = 0
        return created_board

    def is_valid_move(self, player: Player, position: int) -> bool:
        return True if position in player.holes and self.board[position] != 0 else False

    def make_move(self, position: int) -> bool:
        self.was_captured = False
        self.landed_on_mancala = False
        beads: int = self.board[position]
        self.board[position] = 0
        index: int = position
        while beads > 0:
            index = (index + 1) % 14

            if index == self.get_opponent().mancala_spot:
                continue

            # capture opponent holes
            if index in self.current_player.holes and self.board[index] == 0 and beads == 1:
                self.board[self.current_player.mancala_spot] += 1

                flipped_index: int = self.get_opponent().holes[self.current_player.holes.index(index)]
                self.board[self.current_player.mancala_spot] += self.board[flipped_index]
                if self.board[flipped_index] != 0: self.was_captured = True
                self.board[flipped_index] = 0

                if sum(self.board[1:7]) == 0 and self.current_player == self.player_b:
                    self._last_captured = True
                elif sum(self.board[8:]) == 0 and self.current_player == self.player_a:
                    self._last_captured = True

                return False

            self.board[index] += 1
            beads -= 1

        if index == self.current_player.mancala_spot:
            self.landed_on_mancala = True
            return True

        return False


    def can_check_winner(self) -> bool:
        return True if sum(self.board[1:7]) == 0 or sum(self.board[8:]) == 0 else False

    def get_winner(self) -> Optional[Player]:
        if self.board[0] == self.board[7]: return None
        return self.player_b if self.board[0] > self.board[7] else self.player_a

    def tally_score(self) -> None:
        if self._last_captured: self.swap_players()
        total_points: int = sum(self.board[1:7] + self.board[8:])

        for index in range(14):
            if index == self.current_player.mancala_spot: self.board[index] += total_points
            elif index == self.get_opponent().mancala_spot: continue
            else: self.board[index] = 0

        if self._last_captured: self.swap_players()

    def swap_players(self) -> None:
        self.current_player = self.get_opponent()

    def get_opponent(self) -> Player:
        return self.player_a if self.current_player == self.player_b else self.player_b

    def print_board(self) -> None:
        print("\033[0;107m\033[1;91m" + " " * 8 + self._format_row([x for x in range(13, 7, -1)]) + "\033[0m")
        print("\033[0;107m\033[1;91m" + "-" * 8 * 7 + "\033[0m")
        print("\033[0;107m\033[1;91m" + self._format_row(["B:"] + self.board[14:7:-1]) + "\033[0m")
        print("\033[0;107m\033[1;91m" + f"{self.board[0]:^8}{' ' * 8 * 5}\033[1;94m{self.board[7]:^8}" + "\033[0m")
        print("\033[0;107m\033[1;94m" + self._format_row(["A:"] + self.board[1:7]) + "\033[0m")
        print("\033[0;107m\033[1;94m" + "-" * 8 * 7 + "\033[0m")
        print("\033[0;107m\033[1;94m" + " " * 8 + self._format_row([x for x in range(1, 7)]) + "\033[0m")

    @staticmethod
    def _format_row(row: List[Any]) -> str:
        return "".join([f"{x:<8}" for x in row])

board = Board()


while True:
    os.system('clear')
    board.print_board()
    if board.was_captured: print(f"\033[1;93mPlayer {board.get_opponent().name} captured opponent's beads!\033[0m")
    if board.landed_on_mancala: print(f"\033[1;93mPlayer {board.current_player.name} landed on mancala! Go again.\033[0m")
    print(f"Players {board.current_player.name}'s Turn!")
    print(f"Possible moves: {board.current_player.possible_holes()}")
    while True:
        try:
            move = int(input("Select a hole: "))
            if not board.is_valid_move(board.current_player, move):
                print("Invalid move!")
                continue

            elif board.make_move(move):
                break

            if not board.can_check_winner():
                board.swap_players()
            break
        except ValueError: print("Invalid type!")

    if board.can_check_winner():
        board.tally_score()
        os.system('clear')
        board.print_board()
        if board.was_captured: print(f"\033[1;93mPlayer {board.current_player.name} captured opponent's beads!\033[0m")
        print("Draw!") if board.get_winner() is None else print(f"Player {board.get_winner().name} wins!")
        break
