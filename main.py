import pygame
import numpy
import math
import random
import pickle

pygame.init()
n,m = 150,160
WINDOW = pygame.display.set_mode((n*5,n*5))
playing = True
play = False
mouse = False
symbol = False
k = False

matrix = numpy.zeros((n,n),dtype=bool)
matrix_copy = matrix.copy()
history = []
blue_transparent = (0,0,255,100)
base_pos = (0,0)
for row in range(n):
    for column in range(n):
        #a = random.randint(0,20)
        #if a != 20:
        #    a = False
        #else: a = False
        a = False
        matrix[row][column] = a
def get_w_and_h_and_text(text):

    w = ""
    h = ""
    text_final = ''
    step = 0
    for i in text:
        if i == ' ':
            step += 1
        elif step == 0:
            w += i
        elif step == 1:
            h += i
        elif step == 2:
            text_final+=i
    w,h = int(w),int(h)
    return w,h,text_final
def get_tile(pos):
    x = math.floor(pos[0]/5)
    y = math.floor(pos[1]/5)
    return x,y
def get_pos(row,column,down=False):
    x = row * 5
    y = column * 5
    if down:
        x+=5
        y+=5
    return [x,y]

def summing(row,column,sum):
    try:
        if matrix[row][column]:
            sum += 1
    except:
        pass
    return sum
def check(row,column):
    sum = 0
    sum = summing(row+1,column,sum)
    sum = summing(row + 1, column+1, sum)
    sum = summing(row , column+1, sum)
    sum = summing(row -1, column, sum)
    sum = summing(row -1, column-1, sum)
    sum = summing(row , column-1, sum)
    sum = summing(row + 1, column-1, sum)
    sum = summing(row -1, column+1, sum)
    return sum
def update(matrix,matrix_copy):
    for row in range(n):
        for column in range(n):
            value = matrix[row][column]
            neighbors = check(row,column)
            if not value and neighbors == 3:
                matrix_copy[row][column] = True
            elif value:
                if not (neighbors in {2, 3}):
                    matrix_copy[row][column] = False
                else:
                    matrix_copy[row][column] = True
    history.append(matrix)

    if len(history) >= 1000:
        del history[0]

    matrix = matrix_copy.copy()

    return matrix, matrix_copy
clock = pygame.time.Clock()
while playing:
    WINDOW.fill((0,0,0))

    if play:
        clock.tick(1000)
        print(clock.get_fps())
        matrix, matrix_copy = update(matrix,matrix_copy)
    for row in range(n):
        for column in range(n):
            color = int(matrix[row][column])*255
            pygame.draw.rect(WINDOW,(color,color,color),(row*5,column*5,5,5))
    if mouse:
        pos = pygame.mouse.get_pos()
        row, column = get_tile(pos)
        if not k:
            matrix[row][column] = symbol
        else:
            x_end,y_end = get_pos(row,column,down=True)
            w,h = x_end - base_pos[0], y_end - base_pos[1]
            surface = pygame.surface.Surface((w,h),pygame.SRCALPHA)
            surface.fill(blue_transparent)
            WINDOW.blit(surface, base_pos)
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
            pygame.quit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_k:
                k = True
            if e.key == pygame.K_s:
                matrix, matrix_copy = update(matrix,matrix_copy)
            if e.key == pygame.K_TAB:
                filename = input("Name of file to create")
                f = open(filename,'w+')
                numbers = ""
                for row in range(n):
                    for column in range(n):
                        numbers += str(int(matrix[row][column]))
                f.write(numbers)
                f.close()
            if e.key == pygame.K_v:
                filename = input("Name of the file saved")
                rot = input("Rotate ?")
                pos = pygame.mouse.get_pos()
                left,up = get_tile(pos)
                try:
                    f = open(filename,'r+')
                    text = f.read()
                    w,h,text = get_w_and_h_and_text(text)
                    right,down = w+left-1,h+up-1
                    index = 0
                    matrix_copy = numpy.zeros((w,h),dtype=bool)
                    for row in range(left,right+1):
                        for column in range(up,down+1):
                            value = bool(int(text[index]))
                            index += 1
                            matrix[row][column] = value
                    matrix_copy = matrix.copy()
                except FileNotFoundError:
                    print("This file does not exist.")
            if e.key == pygame.K_l:
                filename = input("Name of file to load")
                try:
                    f = open(filename, 'r')
                    text = f.read()
                    for row in range(n):
                        for column in range(n):
                            number = row * n + column
                            value = int(text[number])
                            matrix[row][column] = value
                    matrix_copy = matrix.copy()
                    f.close()
                except FileNotFoundError:
                    print("The file does not exist.")

            if e.key == pygame.K_SPACE:
                play = not play
            if e.key == pygame.K_z:
                try:
                    matrix = history[-1]
                    del history[-1]
                    matrix_copy = matrix.copy()
                except:
                    pass
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_k:
                k = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse = True
            row,column = get_tile(e.pos)
            if not k:
                symbol = not matrix[row][column]
                matrix[row][column] = not matrix[row][column]
            if k:
                base_pos = get_pos(row,column)

        if e.type == pygame.MOUSEBUTTONUP:
            mouse = False
            if k:
                left,up = get_tile((base_pos[0]+1,base_pos[1]+1))
                right, down = get_tile((e.pos[0],e.pos[1]))
                w,h = right-left+1,down-up+1
                figure = f"{w} {h} "
                for row in range(left,right+1):
                    for column in range(up,down+1):
                        figure += str(int(matrix[row][column]))
                file = input("Name of the file where you want to save it :\n")
                f = open(file,'w+')
                f.write(figure)
                f.close()