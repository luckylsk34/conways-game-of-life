#!/usr/bin/env python3
"""this module simulates the conway's game of life"""

import os
import sys
import time
from PIL import Image
import imageio


def print_game(game, length, breadth):
    """this function prints each game given to it"""
    for i in range(1, breadth+1):
        for j in range(1, length+1):
            print(game[i][j], end=" ")
        print("")


def pop(game, i_pos, j_pos):
    """this function calculates the population around a given node"""
    top = game[i_pos-1][j_pos-1] + \
        game[i_pos-1][j_pos] + game[i_pos-1][j_pos+1]
    level = game[i_pos][j_pos-1] + game[i_pos][j_pos+1]
    bottom = game[i_pos+1][j_pos-1] + \
        game[i_pos+1][j_pos] + game[i_pos+1][j_pos+1]
    return top+level+bottom


def store_game(game, game_l, game_b):
    """this function stores the game into an png image"""
    im = Image.new('RGB', (game_l*4, game_b*4))
    for j in range(0, game_b):
        for i in range(0, game_l):
            im.putpixel((4*i, 4*j), (game[j][i]*255, 0, 0))
            im.putpixel((4*i, 4*j+1), (game[j][i]*255, 0, 0))
            im.putpixel((4*i, 4*j+2), (game[j][i]*255, 0, 0))
            im.putpixel((4*i, 4*j+3), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+1, 4*j), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+1, 4*j+1), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+1, 4*j+2), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+1, 4*j+3), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+2, 4*j), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+2, 4*j+1), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+2, 4*j+2), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+2, 4*j+3), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+3, 4*j), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+3, 4*j+1), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+3, 4*j+2), (game[j][i]*255, 0, 0))
            im.putpixel((4*i+3, 4*j+3), (game[j][i]*255, 0, 0))
    im.save("tmp.png")
    im.close()
    im = imageio.imread("tmp.png")
    return im


def start_game(game, length, breadth, sleep_time, number_of_iterations, is_terminal):
    """this function simulates the conway's game of life"""
    im_array = []
    for x in range(number_of_iterations):
        if(is_terminal):
            print("game-%d" %(x+1))
            print_game(game, length, breadth)
        else:
            im_array.append(store_game(game, length, breadth))
        store_game(game, length+2, breadth+2)
        tmp = [[0 for i in range(0, length+2)] for i in range(0, breadth+2)]
        for i in range(1, breadth+1):
            for j in range(1, length+1):
                l = pop(game, i, j)
                if l < 2 or l > 3:
                    tmp[i][j] = 0
                if l == 2:
                    tmp[i][j] = game[i][j]
                if l == 3:
                    tmp[i][j] = 1
        game = tmp
        time.sleep(sleep_time)
    if is_terminal == 0:
        imageio.mimsave("tmp.gif", im_array, duration=0.5)
        os.remove("tmp.png")
        


def load_game(initial_game, initial_l, initial_b, empty_game, empty_l, empty_b):
    """this function loads the initial game into the empty game"""
    for i in range(initial_b):
        for j in range(initial_l):
            empty_game[(empty_b-initial_b)//2 +
                       i][(empty_l-initial_l)//2+j] = initial_game[i][j]


def load_input():
    """this function loads the input file and parses it to an array"""
    f = open("input.txt")
    tmp = []
    l = 0
    b = 0
    for i in f.readlines():
        tmp.append([int(j) for j in i.split(" ")])
        b += 1
    return [tmp, tmp[0].__len__(), b]


if __name__ == "__main__":

    L = 20
    B = 20
    EMPTY_GAME = [[0 for i in range(0, L+2)] for j in range(0, B+2)]

    INITIAL_GAME, INITIAL_L, INITIAL_B = load_input()

    if sys.argv.__len__() == 4:
        print("total number of iterations:", sys.argv[1])
        print("y for GIF, n for terminal: ", sys.argv[2])
        print("time between each game:", sys.argv[3])
        TOTAL_NUMBER_OF_ITERATIONS = int(sys.argv[1])
        TIME_BETWEEN_EACH_GAME = int(sys.argv[3])
        if sys.argv[2] == 'y':
            TERMINAL = 0
        else:
            TERMINAL = 1
    else:
        TOTAL_NUMBER_OF_ITERATIONS = int(input("total number of iterations: "))
        if input("y for GIF, n for terminal: ") == 'y':
            TERMINAL = 0
        else:
            TERMINAL = 1
        TIME_BETWEEN_EACH_GAME = int(input("time between each game: "))

    load_game(INITIAL_GAME, INITIAL_L, INITIAL_B, EMPTY_GAME, L, B)
    print("initial game:")
    print_game(EMPTY_GAME, L, B)
    start_game(EMPTY_GAME, L, B, TIME_BETWEEN_EACH_GAME,
               TOTAL_NUMBER_OF_ITERATIONS, TERMINAL)
