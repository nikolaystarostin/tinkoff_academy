import random
import pickle
from sys import exit

class Sudoku:
    #starting the game
    def start(self):
        print('Welcome to the Sudoku by Nikolay Starostin!')
        print('To begin please enter how many cells do you want to be filled before the start (from 0 to 81)')
        print('Please do not enter big numbers (>50) or generation will take a lot of time')
        print('Or type "continue" to load saved game')
        self.take_n()
        print('Now you can start: type "row column number" (e.g. 4 3 5) to fill the cell.')
        print('Type "solve" to solve (works not so good)')
        print('Type "save" to save game')
        self.draw_board()

    #take n for generation
    def take_n(self):
        self.n_fill = input()
        if self.n_fill == 'continue':
            self.load()
        elif int(self.n_fill) < 0 or int(self.n_fill) > 81:
            print('Wrong input, try again')
            self.take_n()
        else:
            self.generate_board()

    #save game
    def save(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self.b, f)
        value = input('Do you want to quit? Y/N')
        if value == 'Y':
            exit()
        elif value == 'N':
            self.start()
        else:
            self.save()

    #load game
    def load(self):
        with open('data.pickle', 'rb') as f:
            self.b = pickle.load(f)
        self.draw_board()

    #generate board
    def generate_board(self):
        self.b = ['         ', '         ', '         ',
                  '         ', '         ', '         ',
                  '         ', '         ', '         ']
        i = 0
        while i < int(self.n_fill):
            r, c, n = [random.randint(1,9), random.randint(1,9), random.randint(1,9)]
            n = str(n)
            row = list(self.b[r-1])
            if row[c-1] == ' ':
                col = [x[c-1] for x in self.b]
                block_r = r // 3
                block_c = c // 3
                block = [x[block_c * 3:block_c * 3 + 3] for x in self.b[block_r * 3:block_r * 3 + 3]]
                block = list(''.join([''.join(x) for x in block]))
                if (n in col) or (n in row) or (n in block):
                    continue
                else:
                    row[c-1] = n
                    self.b[r - 1] = ''.join(row)
                    i += 1
            else:
                continue

    #draw (render) board
    def draw_board(self):
        self.draw_b = [list(x) for x in self.b]
        self.draw_b = ['|'+x[0]+x[1]+x[2]+'|'+x[3]+x[4]+x[5]+'|'+x[6]+x[7]+x[8]+'|' for x in self.draw_b]
        print('-------------')
        print(*self.draw_b[0:3], sep='\n')
        print('-------------')
        print(*self.draw_b[3:6], sep='\n')
        print('-------------')
        print(*self.draw_b[6:9], sep='\n')
        print('-------------')
        if any([' ' in x for x in self.b]):
            self.take_input()
        else:
            print('Congratulations! Want to play again? Y/N')
            self.win()

    #simple solver which works (sometimes)
    def solve_game(self):
        new_board = self.b
        for r in range(9):
            row = list(new_board)[r]
            for c in range(9):
                if row[c] == ' ':
                    i = 1
                    while row[c] == ' ':
                        n = str(i)
                        row = list(new_board[r])
                        if row[c] == ' ':
                            col = [x[c] for x in new_board]
                            block_r = (r) // 3
                            block_c = (c) // 3
                            block = [x[block_c * 3:block_c * 3 + 3] for x in new_board[block_r * 3:block_r * 3 + 3]]
                            block = list(''.join([''.join(x) for x in block]))
                            #if (r == 2) and (c == 2):
                            #    print(row)
                            #    print(col)
                            #    print(block)
                            if (n in col) or (n in row) or (n in block):
                                i += 1
                            else:
                                row[c] = n
                                new_board[r] = ''.join(row)

            self.b = new_board

    #input for filling cells
    def take_input(self):
        self.value = input()
        if self.value == 'solve':
            self.solve_game()
            self.draw_board()
        elif self.value == 'save':
            self.save()
        else:
            self.row, self.col, self.num = map(int, self.value.split())
            if (self.row not in range(1, 10)) or (self.col not in range(1, 10)) or (self.num not in range(1, 10)):
                print('Wrong input, try again')
                self.take_input()
            else:
                self.num = str(self.num)
                self.check_input()

    #checking input to fit with conditions (rows, columns, blocks)
    def check_input(self):
        row = list(self.b[self.row-1])
        print(row)
        if row[self.col-1] == ' ':
            col = [x[self.col-1] for x in self.b]
            block_r = self.row // 3
            block_c = self.col // 3
            block = [x[block_c*3:block_c*3+3] for x in self.b[block_r*3:block_r*3+3]]
            block = list(''.join([''.join(x) for x in block]))
            if self.num in col:
                print('Oops, this number is already in the column, try again')
                self.take_input()
            elif self.num in row:
                print('Oops, this number is already in the row, try again')
                self.take_input()
            elif self.num in block:
                print('Oops, this number is already in the block, try again')
                self.take_input()
            else:
                row[self.col - 1] = str(self.num)
                self.b[self.row - 1] = ''.join(row)
                self.draw_board()
                self.take_input()
        else:
            print('There is a number in this place already')
            self.take_input()

    #if all cells are not empty
    def win(self):
        answer = input()
        if answer == 'Y':
            self.start()
        elif answer == 'N':
            exit()
        else:
            print('Wrong input')
            self.win()


game = Sudoku()
game.start()
