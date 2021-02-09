#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 00:45:44 2021

@author: nikhil
"""

import pygame
import math
from queue import PriorityQueue
import random
from queue import Queue
pygame.init()

WIDTH = 600
HEIGHT = 400
WIN = pygame.display.set_mode((510,400))
pygame.display.set_caption("Select Starting And Target point using mouse left button")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
MAROON = (128,0,0)
XYZ =(0,51,51)

buttonX = 400
buttonY = 5
buttonWidth = 100
buttonHeight = 45
buttonY2 = buttonY + buttonHeight + 20
buttonY3 = buttonY2 + buttonHeight + 20
buttonY4 = buttonY3 + buttonHeight + 20
buttonY5 = buttonY4 + buttonHeight + 20
buttonY6 = buttonY5 + buttonHeight + 20

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row=row
        self.col=col
        self.x=row*width
        self.y=col*width
        self.color=WHITE
        self.neighbors=[]
        self.width=width
        self.height=HEIGHT
        self.total_rows=total_rows
        
    def get_pos(self):
        return self.row,self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color = WHITE
    
    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = TURQUOISE
        
    def make_open(self):
        self.color = XYZ
        
    def make_barrier(self):
        self.color = BLACK
        
    def make_end(self):
        self.color = MAROON
    
    def make_path(self):
        self.color = PURPLE
        
    def make_clear(self):
        self.color = WHITE
        
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,400))
    
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])  
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False
    
    
def h(p1,p2):
    x1,y1= p1
    x2,y2= p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def djikstras(draw, grid, start, end):
	
	count = 0

	min_heap = PriorityQueue()
	
	min_heap.put((0,count,start))
	min_heap_set = {start}
	
	visited = {start}
	
	came_from = {}

	distance = {spot : float("inf") for row in grid for spot in row}
	distance[start] = 0


	while(not min_heap.empty()):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()


		current = min_heap.get()[2]
		min_heap_set.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end() 
			return True

		for neighbor in current.neighbors:

			temp_distance = distance[current]+1
			
			if(temp_distance < distance[neighbor]):

				came_from[neighbor] = current
				distance[neighbor] = temp_distance

				if(neighbor not in min_heap_set):
					count +=1
					min_heap.put((distance[neighbor],count, neighbor))
					min_heap_set.add(neighbor)
					neighbor.make_open()

		draw()

		if(current!= start):
			current.make_closed()


	return False        
def breadthfirstsearch(draw, grid, start, end):
	
	count = 0

	q = Queue()
	qset = {start}

	q.put(start)

	came_from = {}

	while(not q.empty()):

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

		n = q.qsize()

		for i in range(n):

			current = q.get()

			if(current == end):
				reconstruct_path(came_from, end, draw)
				start.make_start()
				end.make_end()
				return True

			for neighbor in current.neighbors:

				if(neighbor not in qset):
					q.put(neighbor)
					neighbor.make_open()
					qset.add(neighbor)
					came_from[neighbor] = current

			draw()

			if(current!=start):
				current.make_closed()

	return False

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot= Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid    

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows+1):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
    for j in range(rows+1):
        pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))
        

     
def draw(win,grid,rows,width):
    win.fill(GREY)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
            
    draw_grid(win,rows,width)
    
    
    
    pygame.draw.rect(win, BLACK,(buttonX,buttonY,buttonWidth+5,buttonHeight))
    pygame.draw.rect(win, BLACK,(buttonX,buttonY2,buttonWidth+5,buttonHeight))
    pygame.draw.rect(win, BLACK,(buttonX,buttonY3,buttonWidth+5,buttonHeight))
    pygame.draw.rect(win, BLACK,(buttonX,buttonY4,buttonWidth+5,buttonHeight))
    pygame.draw.rect(win, BLACK,(buttonX,buttonY5,buttonWidth+5,buttonHeight))
    pygame.draw.rect(win, BLACK,(buttonX,buttonY6,buttonWidth+5,buttonHeight))
    
    font = pygame.font.Font('freesansbold.ttf', 32)
  

    text = font.render('A_*', True, WHITE)
    win.blit(text, (buttonX+25 , buttonY+8)) 
    text = font.render('BFS', True, WHITE)
    win.blit(text, (buttonX+20 , buttonY2+8))
    font = pygame.font.Font('freesansbold.ttf', 27)
    text = font.render('Dijkstra', True, WHITE)
    win.blit(text, (buttonX, buttonY3+8)) 
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render('MAZE', True, WHITE)
    win.blit(text, (buttonX+10 , buttonY4+8))
    font = pygame.font.Font('freesansbold.ttf', 28)
    text = font.render('RESET', True, WHITE)
    win.blit(text, (buttonX+5 , buttonY5+8))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('QUIT', True, WHITE)
    win.blit(text, (buttonX+10 , buttonY6+8))
    pygame.display.update()
        
def get_clicked_pos(pos, rows, width):
	gap = 400 // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col
"""def get_clicked_pos(pos,rows,width):
    gap = width//rows
    y,x = pos
    
    row = y // gap
    col = x // gap
    
    return row,col"""
def create_random_maze(grid):
    for i in range(3,18):
        for j in range(3,18):
            grid[i][j].make_barrier()


def main(win, width):
    
    ROWS = 30
    grid =make_grid(ROWS,400)
    
    
    start = None
    end = None
    
    run = True
   
    
    while run:
        draw(win,grid,ROWS,400)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
           
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if pos[0] < 400:
                     row,col=get_clicked_pos(pos,ROWS,400)
                     spot = grid[row][col]
                print(pos[0])
                print(pos[1])
                if pos[0] > buttonX and pos[0] < buttonX + buttonWidth:
                    if pos[1] > buttonY and pos[1] < buttonY + buttonHeight and start and end:
                           for row in grid: 
                               for spot in row:
                                   spot.update_neighbors(grid)       
                           algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                    elif pos[1] > buttonY2 and pos[1] < buttonY2 + buttonHeight and start and end:
                           for row in grid: 
                               for spot in row:
                                   spot.update_neighbors(grid)       
                           breadthfirstsearch(lambda: draw(win, grid, ROWS, width), grid, start, end)
                           
                    elif pos[1] > buttonY3 and pos[1] < buttonY3 + buttonHeight and start and end:
                           for row in grid: 
                               for spot in row:
                                   spot.update_neighbors(grid)       
                           djikstras(lambda: draw(win, grid, ROWS, width), grid, start, end)
               
                    elif pos[1] > buttonY4 and pos[1] < buttonY4 + buttonHeight:
                         for i in range(20):
                             r = random.randrange(len(grid))
                             c = random.randrange(len(grid))
                             if grid[r][c]!=start and grid[r][c]!= end:
                                     grid[r][c].make_barrier()
                                  
                    elif pos[1] > buttonY5 and pos[1] < buttonY5 + buttonHeight:
                           for row in grid: 
                               for spot in row:
                                   spot.make_clear()   
                                   start = None
                                   end = None
                                   
                    elif pos[1] > buttonY6 and pos[1] < buttonY6 + buttonHeight:
                              pygame.display.quit()
                    
                elif pos[0] > 0 and pos[0] < 400 and not start and spot!=end:
                    if pos[1] > 0 and pos[1] < 400:
                        start= spot
                        start.make_start()
                    
                    
                elif pos[0] > 0 and pos[0] < 400 and not end and spot!=start:
                     if pos[1] > 0 and pos[1] < 400:
                          end = spot
                          end.make_end()
                    
                    
                elif pos[0] > 0 and pos[0] < 400 and spot!= end and spot != start:
                    if pos[1] > 0 and pos[1] < 400:
                          spot.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]:
                 pos = pygame.mouse.get_pos()
                 row,col=get_clicked_pos(pos,ROWS,width)
                 spot = grid[row][col]
                 spot.reset()
                 if spot== start:
                     start = None
                 elif spot == end:
                     end = None
            

                     
               
                
                
    pygame.quit()
main(WIN,500)
        
        
    

        