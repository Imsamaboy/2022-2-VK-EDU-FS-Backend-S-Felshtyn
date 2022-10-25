from exceptions.InputException import InputException


class TicTacToeGame:
    """
    Class for Tic-Tac-Toe game
    """
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.pos = {'X': [], 'O': []}
        self.opt = ['X', 'O']
        self.players = {}

    def show_board(self, ) -> None:
        """
        This method prints current board status
        :return: None
        """
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board[0], self.board[1], self.board[2]))
        print('\t_____|_____|_____')
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board[3], self.board[4], self.board[5]))
        print('\t_____|_____|_____')
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board[6], self.board[7], self.board[8]))
        print("\t     |     |")
        print("\n")

    def victory_check(self, current_player: str) -> bool:
        """
        This method returns True if current player win
        False otherwise
        :param: current_player: player name that makes current move
        :return: true / false
        """
        solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for solution in solutions:
            if all(combination in self.pos[self.players[current_player]] for combination in solution):
                return True
        return False

    def draw_check(self, ) -> bool:
        """
        This method checks: is it draw now?
        :return: true / false
        """
        return len(self.pos['X']) + len(self.pos['O']) == 9

    @staticmethod
    def validate_input(input_text: str) -> int:
        """
        Validates user input
        Throws exceptions if needed
        :param: input_text: users input
        :return: move block
        """
        move = int(input_text)
        if move < 1 or move > 9:
            raise InputException
        return move

    def start_game(self, ) -> None:
        """
        This method starts the game between 2 players
        Prints who win or draw status
        :return: None
        """
        print("First Player")
        player_1 = input("Specify the Name: ")
        print("\n")
        print("Second Player")
        player_2 = input("Specify the Name: ")
        print("\n")

        self.players[player_1] = "X"
        self.players[player_2] = "O"
        current_player = player_1
        while True:
            self.show_board()

            print("Player ", current_player, " turn. Choose your Block : ", end="")
            try:
                move = self.validate_input(input())
            except ValueError:
                print("Invalid Input! Try again select block (1-9).")
                continue
            except InputException:
                print("Invalid Input! Block can be only from 1 to 9.")
                continue

            if self.board[move - 1] != ' ':
                print("Oops! The Place is already occupied. Try again!!")
                continue

            self.board[move - 1] = self.players[current_player]
            self.pos[self.players[current_player]].append(move)

            if self.victory_check(current_player):
                self.show_board()
                print("Congratulations! Player ", current_player, " has won the game!")
                print("\n")
                break

            if self.draw_check():
                self.show_board()
                print("Oh! Draw!")
                print("\n")
                break

            current_player = player_2 if current_player == player_1 else player_1


if __name__ == '__main__':
    game = TicTacToeGame()
    game.start_game()
