def col(x):
    return {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }.get(x)


def row(x):
    return {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0,
    }.get(x)


def col_rev(x):
    return {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
    }.get(x)


def row_rev(x):
    return {
        0: "8",
        1: "7",
        2: "6",
        3: "5",
        4: "4",
        5: "3",
        6: "2",
        7: "1",
    }.get(x)


class StanGry:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.turn = True
        self.game = False

    def rusz(self, ruch):
        col_one = ruch[0]
        row_one = ruch[1]
        col_two = ruch[2]
        row_two = ruch[3]

        self.board[row(row_two)][col(col_two)] = self.board[row(row_one)][col(col_one)]
        self.board[row(row_one)][col(col_one)] = "--"

    def rusz_rev(self, ruch):
        self.board[ruch[1][0]][ruch[1][1]] = self.board[ruch[0][0]][ruch[0][1]]
        self.board[ruch[0][0]][ruch[0][1]] = "--"
