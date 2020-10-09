import sys
from sudoku import Sudoku

HEIGHT = 9
WIDTH = 9

def main():

    # Ensure proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python runner.py file")

    # Get a game from a file
    filename = sys.argv[1]
    with open(filename) as f:
        contents = f.read()

    # Assemble a board (9x9 array) with the data
    contents = contents.splitlines()
    board = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            try:
                row.append(int(contents[i][j]))
            except:
                row.append(False)
        board.append(row)
    #print(board)

    #Starts a new game object
    #game = Sudoku(height=HEIGHT, width=WIDTH)
    game = Sudoku(board, height=HEIGHT, width=WIDTH)
    print("Game:")
    game.print()

    #Try to solve the game
    game.solve()



if __name__ == "__main__":
    main()
