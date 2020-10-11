import pygame
import random
import os
import copy
import time
from tkinter import *

#Tkinter window to select game variables

#Default game variables
time = 4
toroid_size = 20
size = 600




#Tkinter window
root = Tk()

myvar = StringVar(); myvar1 = StringVar(); myvar2 = StringVar()


def update_variables():
    global time, toroid_size, size

    time = int(myvar2.get())
    toroid_size = int(myvar1.get())
    size = int(myvar.get())

    root.destroy()


#Label frame for aesthetic purposes
label_frame = LabelFrame(root, text = 'Personalize game')
label_frame.pack()


#Entry names
Label(label_frame, text = 'Window Size (NxN): ').grid(row = 0, column = 0)
Label(label_frame, text = 'Grid Size (NxN): ').grid(row = 1, column = 0)
Label(label_frame, text = 'Ticks per second: ').grid(row = 2, column = 0)


#Entries
window_size_entry = Entry(label_frame, width = 20,textvariable = myvar)
grid_size_entry = Entry(label_frame, width = 20, textvariable = myvar1)
tick_speed_entry = Entry(label_frame, width = 20, textvariable = myvar2)


myvar.set('600')
myvar1.set('20')
myvar2.set('4')


window_size_entry.grid(row = 0, column = 1)
grid_size_entry.grid(row = 1, column = 1)
tick_speed_entry.grid(row = 2, column = 1)


#Start button
Button(label_frame, text = 'Start game', command = update_variables).grid(row = 3, column = 1)


root.mainloop()







#Basic pygame initialization code and variables
pygame.init()

window_width, window_height = size, size

game_display = pygame.display.set_mode((window_width, window_height))


clock = pygame.time.Clock()


white = (255, 255, 255)
black = (0, 0, 0)

alive_color = black
dead_color = white

class Toroid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

        #Creates a completely dead (false) board
        self.board = [[False for i in range(self.columns)] for i in range(self.rows)]
        self.original_board = [[False for i in range(self.columns)] for i in range(self.rows)]



    def switch_state(self, row, column):
        #Switches the boolean value (From dead to alive and viceversa)
        self.board[row][column] = not self.board[row][column]
        self.original_board[row][column] = not self.original_board[row][column]



    def tick(self):
        #Loops through every coordinate
        for row in range(self.rows):
            for column in range(self.columns):

                #Alive position cases
                if self.original_board[row][column]:

                    #Only situation where an alive position remains alive after a tick (has 2 or 3 neighbors)
                    if 2 <= self.alive_neighbors(row, column) <= 3:
                        self.board[row][column] = True

                    else:
                        self.board[row][column] = False


                #Dead position cases
                else:

                    #Only situation where a dead position becomes alive (has exactly 3 neighbors)
                    if 3 == self.alive_neighbors(row, column):
                        self.board[row][column] = True

                    else:
                        self.board[row][column] = False



        self.original_board = copy.deepcopy(self.board)
        



    def alive_neighbors(self, row, column):
        alive_coordinates = 0


        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):

                cyclic_row, cyclic_column = r % self.rows, c % self.columns


                if not (r == row and c == column) and self.original_board[cyclic_row][cyclic_column]:
                    alive_coordinates += 1


        return alive_coordinates



    #Print function created for reading the board easily
    def print(self):
        for row in self.board:
            print(row)



    #Draws board to Pygame game display
    def draw_board(self):
        block_size = int(window_width / self.rows)

        for row in range(self.rows):
            for column in range(self.columns):

                rect = pygame.Rect(row * block_size, column * block_size, block_size, block_size)

                #If position is alive then draw black square
                if self.board[column][row]:
                    pygame.draw.rect(game_display, alive_color, rect)

                #Otherwise draw white square
                else:
                    pygame.draw.rect(game_display, dead_color, rect)




class Game:
    def __init__(self):
        pass


    def run(self):
        #Toroid object
        toroid = Toroid(toroid_size, toroid_size)

        #Loop variables
        ticking = False


        #Game loop
        while True:
            #For loop that iterates over game events
            for event in pygame.event.get():

                #To quit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                #Lets the user set which positions are alive or dead
                if event.type == pygame.MOUSEBUTTONDOWN and not ticking:
                    position = pygame.mouse.get_pos()
                    block_size = int(window_width / toroid.rows)

                    row = position[1] // block_size
                    column = position[0] // block_size

                    toroid.switch_state(row, column)


                #If a key is pressed the game switches the current ticking state
                if event.type == pygame.KEYDOWN:
                    ticking = not ticking



            toroid.draw_board()


            if ticking:
                toroid.tick()


            clock.tick(time)


            pygame.display.update()



app = Game()
app.run()