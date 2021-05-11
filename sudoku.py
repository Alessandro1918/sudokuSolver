import copy
import sys

class Sudoku():

    def __init__(self, board, height=9, width=9):

        # Set initial width, height
        self.height = height
        self.width = width

        # Get board from argument
        self.board = board

        # List of cells the program figured out the value
        self.added = []
        
        # 9x9 grid with possible values for each cell,
        # based on elimination from different methods and shorted at each iteration
        self.possibles = []
        for i in range(height):
        	row = []
        	for j in range(width):
        	    row.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
        	self.possibles.append(row)


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
                    #V1 - no color
                    #print(f" {self.board[i][j]} ", end="")
                    #V2 - colored
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
        
        #print(f"Cell({i}, {j}): {value} - found by {sys._getframe(1).f_code.co_name} method")
        self.board[i][j] = value    # assing value
        self.added.append((i, j))   # list of cells I figured out the value; will be printed red
        self.possibles[i][j] = []       # if cell is now filled, it has no possible list of values. Like getCellPossibles(someFilledCell) will return []
        
        # updates the 'possibles' of all the cells from the same row, collumn, box
        for m in range(self.height):
                for n in range(self.width):
                    # the cell is in the same row, collumn or box of the cell I just figured out the value
                    if i == m or j == n or self.getSectionCenter(i, j) == self.getSectionCenter(m, n):
                        # if they have among their 'possibles' the 'value' I know they can't have, remove that value
                        try:
                            index = self.possibles[m][n].index(value)
                        except:
                            index = -1
                        if index > -1:
                            self.possibles[m][n].pop(index)

                            
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


    # Returns a list of values this cell CAN have,
    # based on the values the other cells from the same row, collumn and section have
    def getCellPossibles(self, i, j):

        # Cell has value (given or figured out)
        if self.board[i][j]:
            #return [self.board[i][j]]      # V1 - cell already has a value; if I return a list with len = 1, Method 1 will color it red
            return []                       # V2 - given or figured out, nothing more to do with this cell

        # Remove from a complete list the values I know to be impossible
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for impossible in self.getImpossibles(i, j):
            if impossible in values:
                    values.pop(values.index(impossible))

        return values


    # Returns a list os values that each cell of that line (row / collumn) can have
    def getLinePossibles(self, i, isRow):
        values = []
        for j in range(9):
            if isRow:
                values.append(self.getCellPossibles(i, j))  # row
            else:
                values.append(self.getCellPossibles(j, i))  # collumn
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
    
    
    # Compare each element from two 9x9 lists to see if any element from list 1 is shorter than their counterpart from list 2
    # List 1: List of possible values each cell can have at the END of the iteration
    # List 2: List of possible values each cell could have at the START of the iteration
    # If True, some method reduced the set of possible values for one or more cells. Breaks loop at first difference
    def isShorter(self, list1, list2):
        for i in range(9):
            for j in range(9):
                if len(list1[i][j]) < len(list2[i][j]):
                    #print(f"End of iteration; list possible values is shorter at, among other cells, ({i}, {j}): from {list2[i][j]} to {list1[i][j]}")
                    return True
        return False

    
    
    # Method 1 - Naked singles
    # for each cell - check if it can have just one possible value
    def nakedSingles(self, i, j):

    	#V1 - eval possibles from scratch
        #values = self.getCellPossibles(i, j)

        #V2 - use a set of possibles already reduced by other methods
        v1 = self.getCellPossibles(i, j)
        v2 = self.possibles[i][j]
        # get alternative with shortest list
        values = v1 if len(v1) < len(v2) else v2
        #print(f"{iterations}: Values for ({i}, {j}): {values}")
        # update class var with shortest list
        self.possibles[i][j] = values
        if len(values) == 1:
            self.write(i, j, values[0])
     
    
    
    # Method 2 - Single value in the area (row, collumn, section)
    # 2.1: for each line row - any cell from that line could have a value that no other cell in that line could have?
    # 2.2: for each collumn - any cell from that collumn could have a value that no other cell in that collumn could have?
    # Params:
    # isRow: if the line is a row (fixed i, iterate j) or collumn (iterate i, fixed j)
    # i: iterator index of that line
    # line: a 1x9 list of possible values for that row or collumn
    def singleValueInTheLine(self, isRow, i, line):

        # example with 2.txt, row 2:
        # only cell (2, 5) in this row could have the value 4
        #row = self.getRowPossibles(i)
        #print(f"row {i}: {row}")          # row 2: [[1, 8], [], [7, 8], [], [], [1, 4], [], [1, 7], []]

        counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for m in line:
            for n in m:
                counts[n-1]+=1
        #print(f"row {i}: {counts}")        # row 2: [3, 0, 0, 1, 0, 0, 2, 2, 0] -> 3 times the #1, 0 times the #2, ...

        value = 0
        for c in counts:                    # any value was counted just once?
            value +=1
            if c == 1:                      # c = 1 @ value = 4
                for j in range(9):          # which element from that row can be a 4?
                    if value in line[j]:    # row[5] contains a 4 -> j=5
                        if isRow:
                            #print(i, j, value)
                            self.write(i, j, value) # i=2, j=5, value=4
                        else:
                            self.write(j, i, value)

            # Can I apply Method 3 - Box Line Reduction?
            if c == 2 or c == 3:             # value 8 was counted 2 times, 7 too
                self.boxLineReduction(value, c, isRow, i, line)
    
    
    
    # Method 3 - Box Line Reduction
    # https://www.sudokuwiki.org/Intersection_Removal#LBR
    # If we find numbers in any row or column that are grouped together in just one box,
    # we can exclude those numbers from the rest of the box.
    # Shortens the list of possible values each cell can have (class var 'self.possibles')
    # Params:
    # value: one int between 1 - 9
    # count: how many cells can have that value (2 or 3, max)
    # isRow: if the line is a row (fixed i, iterate j) or collumn (iterate i, fixed j)
    # i: iterator index of that line
    # line: a 1x9 list of possible values for that row or collumn
    def boxLineReduction(self, value, count, isRow, i, line):

        # ex: data/7.txt, second-to-last collumn:
        # line: [[4, 9], [4, 7], [], [7, 9], [], [], [], [], []]
        # collumn 7: 2x #4     cells: [(0, 7), (1, 7)]      both from same box
        # collumn 7: 2x #7     cells: [(1, 7), (3, 7)]      different boxes
        # collumn 7: 2x #9     cells: [(0, 7), (3, 7)]      different boxes

        # which pair or trio of cells are we talking about?
        #print("line:", line)
        lineType = "row" if isRow else "collumn"
        #print(f"{lineType} {i}: {count}x #{value}")
        cells = []
        j = -1
        for cell in line:
            j += 1
            if value in cell:
                if isRow:
                    cells.append((i, j))
                else:
                    cells.append((j, i))
        #print("cells:", cells)

        # are they all in the same box?
        # 1. for each cell, get their center
        centers = []
        for cell in cells:
            centers.append(self.getSectionCenter(cell[0], cell[1]))     #cell[0] = i; cell[1] = j
        #print("centers:", centers)
        # 2. all the items from that list are equal?
        sameCenter = True if centers.count(centers[0]) == len(centers) else False
        #print("sameCenter:", sameCenter)

        if sameCenter:

            # for all the cells from that box
            centerRow = centers[0][0]
            centerCollumn = centers[0][1]
            for m in range(centerRow-1, centerRow+2):
                for n in range (centerCollumn-1, centerCollumn+2):

                    # if they are not part of the pair or trio
                    if (m, n) not in cells:
                        #print("i: ", m, "    j:", n, "     possibles:", self.possibles[m][n])

                        # if they have among their 'possibles' the 'value' I know they can't have, remove that value
                        try:
                            index = self.possibles[m][n].index(value)
                        except:
                            index = -1
                        if index > -1:
                            self.possibles[m][n].pop(index)
                            #print(f"({m}, {n}): possibles: {self.possibles[m][n]} - box {lineType} reduced; removed the {value}")
                            #if len(self.possibles[m][n]) == 1:
                            #    print(f"({m}, {n}) box-line reduced to a single value: {self.possibles[m][n][0]}")

        #print("")

        
        
    #https://www.sudokuwiki.org/sudoku.htm
    def solve(self):

        iterations = 0
        
        while not self.isFinished():

            iterations+=1
            #print("\nIteration", iterations)
            quantAdded = len(self.added)                    # loop breaking var - how many cells were added on total after the previous iteration
            oldPossibles = copy.deepcopy(self.possibles)    # loop breaking var - how was the list of possible values for each cell after the previous iteration

            # Method 1 - Naked singles
            # for each cell - check if it can have just one possible value
            for i in range(self.height):
                for j in range(self.width):
                    self.nakedSingles(i, j)
            
            
            # Method 2 - Single value in the area (row, collumn, section)
            
            # 2.1: for each row - any cell from that row could have a value that no other cell in that row could have?
            for i in range(self.height):
                rowPossibles = self.getLinePossibles(i, True)           # getRowPossibles
                self.singleValueInTheLine(True, i, rowPossibles)        # isRow, iterator index, possible values

            # 2.2: for each collumn - any cell from that collumn could have a value that no other cell in that collumn could have?
            for j in range(self.width):
                collumnPossibles = self.getLinePossibles(j, False)      # getCollumnPossibles
                self.singleValueInTheLine(False, j, collumnPossibles)   # isRow, iterator index, possible values

            # 2.3: for each section - any cell from that section could have a value that no other cell in that section could have?
            # example with 2.txt, section 2: only cell (0, 8) in this section could have the value 6
            cells = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]    #the first cell of each section
            for s in range(9):       # section 2 starts @ cell (0, 6)
                i = cells[s][0]      # i = 0
                j = cells[s][1]      # j = 6
                section = self.getSectionPossibles(i, j)
                #print(f"section {s}: {section}")   # section 2: [[], [1, 5, 7], [1, 5, 6, 7], [1, 5], [], [], [], [1, 7], []]
                counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                for m in section:
                    for n in m:
                        counts[n-1]+=1
                #print(f"section {s}: {counts}")    # section 2: [4, 0, 0, 0, 3, 1, 1, 0, 0]
                for c in counts:
                    if c == 1:                      # counts[5] = 1
                        v = counts.index(c) + 1     # singleValue = 5+1 = 6
                        for k in range(9):          # which element from that section can be a 6?
                            if v in section[k]:     # section[2] contains a 6 -> k=2 (meaning it's the third cell from that section)
                                ii = int(i + k / 3) # i = 0 -> ii = 0+2/3 = 0
                                jj = j + k % 3      # j = 6 -> jj = 6+2%3 = 8
                                self.write(ii, jj, v)

                                
            # Just did a whole iteration, and:
            # 1. didn't figured out any new cell values,
            # 2. nor did I reduced the list of possibles values for any cell
            if len(self.added) == quantAdded and not self.isShorter(self.possibles, oldPossibles):
                print(f"Error - Couldn't solve it in {iterations} steps - Added {len(self.added)} cells")
                self.print()
                return

        print(f"Solved in {iterations} steps!")
        self.print()
