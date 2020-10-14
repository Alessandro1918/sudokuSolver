class Sudoku():

    def __init__(self, board, height=9, width=9):

        # Set initial width, height
        self.height = height
        self.width = width

        # Get board from argument
        self.board = board

        # List of cells the program figured out the value
        self.added = []


    # Prints a text-based representation of the board
    def print(self):

        #Use a different color for the cells figured out by the program
        #https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
        CRED = '\033[91m'   # red
        CEND = '\033[0m'    # white

        #board's header
        print("---" * self.width + "----")

        for i in range(self.height):

            #start line
            print("|", end="")

            for j in range(self.width):
                if self.board[i][j]:
                    #print(f" {self.board[i][j]} ", end="") #V1 - no color
                    if (i, j) in self.added:
                        print(CRED + f" {self.board[i][j]} " + CEND, end="")
                    else:
                        print(CEND + f" {self.board[i][j]} " + CEND, end="")
                else:
                    print(" . ", end="")
                if j == 2 or j == 5:
                    print("|", end="")
                if j == 8:
                    print("|")

            #line finished
            if i == 2 or i == 5 or i == 8:
                print("---" * self.width + "----")

        print("\n")


    # Fill some cell from the board with some value
    def write(self, i, j, value):
        
        self.board[i][j] = value    
        self.added.append((i, j))


    # Check if the board is completed
    def isFinished(self):

        for i in range(self.height):
            for j in range(self.width):
                if not self.board[i][j]:
                    return False
        return True


    # Given a cell, returns the center for that cell's section
    def getSectionCenter(self, i, j):
        centerRow = -1
        centerCollumn = -1
        if i == 0 or i == 1 or i == 2: centerRow = 1
        if i == 3 or i == 4 or i == 5: centerRow = 4
        if i == 6 or i == 7 or i == 8: centerRow = 7
        if j == 0 or j == 1 or j == 2: centerCollumn = 1
        if j == 3 or j == 4 or j == 5: centerCollumn = 4
        if j == 6 or j == 7 or j == 8: centerCollumn = 7
        return centerRow, centerCollumn


    # Returns a list of values this cell CAN'T have
    def getImpossibles(self, i, j):

        values = []

        # this values are in the cross of the cell
        for k in range(9):
            values.append(self.board[i][k])
            values.append(self.board[k][j])

        # this values are in the section of the cell
        centerRow, centerCollumn = self.getSectionCenter(i, j)
        for m in range(centerRow-1, centerRow+2):
            for n in range (centerCollumn-1, centerCollumn+2):
                values.append(self.board[m][n])

        return values


    # Returns a list of values this cell CAN have
    def getCellPossibles(self, i, j):

        # Cell is filled
        if self.board[i][j]:
            #return [self.board[i][j]]      # given value; do not highlight
            return []                       # solve will ignore this cell

        # Remove from a complete list the values I know to be impossible
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for impossible in self.getImpossibles(i, j):
            if impossible in values:
                    values.pop(values.index(impossible))

        return values


    # Returns a list os values that each cell of that row can have
    def getRowPossibles(self, i):
        values = []
        for k in range(9):
            values.append(self.getCellPossibles(i, k))
        return values


    # Returns a list os values that each cell of that collumn can have
    def getCollumnPossibles(self, j):
        values = []
        for k in range(9):
            values.append(self.getCellPossibles(k, j))
        return values


    # Returns a list os values that each cell of that section can have
    def getSectionPossibles(self, i, j):
        values = []
        centerRow, centerCollumn = self.getSectionCenter(i, j)
        for m in range(centerRow-1, centerRow+2):
            for n in range (centerCollumn-1, centerCollumn+2):
                v = self.getCellPossibles(m, n)
                values.append(v)
        return values


    #https://www.sudokuwiki.org/sudoku.htm
    def solve(self):

        iterations = 0
        while not self.isFinished():

            iterations+=1
            newValues = 0

            # Method 1 - Naked singles
            #for each cell - check if it can have just one possible value
            for i in range(self.height):
                for j in range(self.width):
                    values = self.getCellPossibles(i, j)
                    #print(f"{k}: Values for ({i}, {j}): {values}")
                    if len(values) == 1:
                        self.write(i, j, values[0])
                        newValues+=1
            
            # Method 2 - Single value in the area (row, collumn, section)
            #for each row - any cell from that row could have a value that no other cell in that row could have?
            # example with 2.txt, row 2: only cell (2, 5) in this row could have the value 4
            for i in range(self.height):
                row = self.getRowPossibles(i)
                #print(i, row)      # row 2: [[1, 8], [], [7, 8], [], [], [1, 4], [], [1, 7], []]
                counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for m in row:
                    for n in m:
                        counts[n-1]+=1
                #print(i, counts)   # row 2: [3, 0, 0, 1, 0, 0, 2, 2, 0] -> 3 times the #1, 0 times the #2, ...
                for c in counts:                    # any value was counted just once?
                    if c == 1:                      # counts[3] == 1
                        v = counts.index(c) + 1     # singleValue = 3+1 = 4
                        for j in range(9):          # which element from that row can be a 4?
                            if v in row[j]:         # row[5] contains a 4 -> j=5
                                #print(i, j, v)
                                self.write(i, j, v) # i=2, j=5, v=4
                                newValues+=1

            #for each collumn - any cell from that collumn could have a value that no other cell in that collumn could have?
            for j in range(self.width):
                collumn = self.getCollumnPossibles(j)
                counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for m in collumn:
                    for n in m:
                        counts[n-1]+=1
                for c in counts:
                    if c == 1:
                        v = counts.index(c) + 1
                        for i in range(9):
                            if v in collumn[i]:
                                self.write(i, j, v)
                                newValues+=1

            #for each section - any cell from that section could have a value that no other cell in that section could have?
            # example with 2.txt, section 2: only cell (0, 8) in this section could have the value 6
            cells = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]    #the first cell of each section
            for s in range(9):       # section 2 starts @ cell (0, 6)
                i = cells[s][0]      # i = 0
                j = cells[s][1]      # j = 6
                section = self.getSectionPossibles(i, j)
                #print(s, section)   # section 2: [[], [1, 5, 7], [1, 5, 6, 7], [1, 5], [], [], [], [1, 7], []]
                counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for m in section:
                    for n in m:
                        counts[n-1]+=1
                #print(s, counts)    # section 2: [4, 0, 0, 0, 3, 1, 1, 0, 0]
                for c in counts:
                    if c == 1:                      # counts[5] = 1
                        v = counts.index(c) + 1     # singleValue = 5+1 = 6
                        for k in range(9):          # which element from that section can be a 6?
                            if v in section[k]:     # section[2] contains a 6 -> k=2 (meaning it's the third cell from that section)
                                ii = int(i + k / 3) # i = 0 -> ii = 0+2/3 = 0
                                jj = j + k % 3      # j = 6 -> jj = 6+2%3 = 8
                                self.write(ii, jj, v)
                                newValues+=1

            # Just did a whole iteration and didn't figured out any new cell values
            if newValues == 0:
                print(f"Error - Couldn't solve it in {iterations} steps")
                self.print()
                return

        print(f"Solved in {iterations} steps!")
        self.print()
