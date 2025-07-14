import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod
from copy import deepcopy

from Dot import *
from Ghost import *
from Pacman import *
from Object import *

# 게임 설정 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

MAX_X = SCREEN_WIDTH//CELL_SIZE
MAX_Y = SCREEN_HEIGHT//CELL_SIZE

OBJECTS = [[Pacman, "pacman"],
           [Ghost, "follow"]
           ]

BLUE = (0, 0, 255)

class Maze:
    """미로 클래스"""
    def __init__(self):
        self.row = 0
        self.col = 0
        self.maze = []
        self.read_txt('./datas/map.txt')
        self.tot_maze = []
        self.make_tot_map()
        
        # 출력상 가장 밑의 index값
        self.y_idx = 0
        self.x_idx = 0
    
    def read_txt(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        self.row, self.col = map(int, lines[0].split())
        
        for line in lines[1:1+self.row]:
            self.maze.append(list(map(int, line.split())))
            
        for i in range(self.row):
            for j in range(self.col):
                if self.maze[i][j] > 3:
                    self.maze[i][j] = [self.maze[i][j],2]
    
    def make_tot_map(self):
        x_cnt = 0
        y_cnt = 0
        while (y_cnt <= MAX_Y):
            x_cnt = 0
            self.tot_maze.append([])
            while (x_cnt <= MAX_X):
                self.tot_maze[y_cnt].append(self.maze[y_cnt%self.row][x_cnt%self.col])
                x_cnt += 1
            y_cnt += 1
        
        # 맵에 객체 추가
        for i in range(MAX_Y+1):
            for j in range(MAX_X+1):
                if type(self.tot_maze[i][j]) != int:
                    # 나중에 상세값 수정
                    self.tot_maze[i][j][0] = OBJECTS[self.tot_maze[i][j][0] - 3][0](0, 0, OBJECTS[self.tot_maze[i][j][0] - 3][1])   # 위치 나중에 수정
    
    
    def shift_map_x(self):
        self.x_idx += 1
        for i in range(MAX_Y):
            if self.tot_maze[i][MAX_X] not in [1,2,3]:
                del self.tot_maze[i][MAX_X]
        for i in range(MAX_X):
            self.tot_maze[:][i] = deepcopy(self.tot_maze[:][i+1])
        y_cnt = 0
        while (y_cnt <= MAX_Y):
            self.tot_maze[y_cnt][MAX_X] = self.maze[(self.y_idx + y_cnt)%self.row][(self.x_idx + MAX_X)%self.col]
            
    def shift_map_y(self):
        self.y_idx += 1
        for i in range(MAX_X):
            if self.tot_maze[MAX_Y][i] not in [1,2,3]:
                del self.tot_maze[MAX_Y][i]
        for i in range(MAX_Y):
            self.tot_maze[i][:] = deepcopy(self.tot_maze[i+1][:])
        x_cnt = 0
        while (x_cnt <= MAX_X):
            self.tot_maze[MAX_Y][x_cnt] = self.maze[(self.y_idx + MAX_Y)%self.row][(self.x_idx + x_cnt)%self.col]            
    
    def draw(self, screen, xgap, ygap):
        x_cnt = 0
        y_cnt = 0
        
        while (y_cnt <= MAX_Y):
            x_cnt = 0
            while (x_cnt <= MAX_X):
                if self.maze[(self.y_idx + y_cnt)%self.row][(self.x_idx + x_cnt)%self.col] == 1:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x_cnt*CELL_SIZE + xgap, y_cnt*CELL_SIZE + ygap, CELL_SIZE, CELL_SIZE))
                x_cnt += 1
            y_cnt += 1
    
    def is_wall(self, row, col):
        if self.maze[row][col] == 1: return True
        else: return False
    
    
    
    
    
    # def __init__(self):
    #     # 미로 레이아웃 (1: 벽, 0: 빈 공간, 2: 점, 3: 파워 펠릿)
    #     self.layout = [
    #         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #         [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    #         [1,3,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,3,1],
    #         [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    #         [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
    #         [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
    #         [1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1],
    #         [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
    #         [1,1,1,1,2,1,0,1,1,0,0,1,1,0,1,2,1,1,1,1],
    #         [0,0,0,0,2,0,0,1,0,0,0,0,1,0,0,2,0,0,0,0],
    #         [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
    #         [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
    #         [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
    #         [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    #         [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
    #         [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
    #         [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
    #         [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
    #         [1,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1],
    #         [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    #         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #     ]
    #     self.dots = []
    #     self.power_pellets = []
    #     self.walls = []
    #     self.load_maze()
    
    # def load_maze(self):
    #     """미로 데이터 로드"""
    #     # TODO: layout을 기반으로 벽, 점, 파워펠릿 객체 생성
    #     for row in range(len(self.layout)):
    #         for col in range(len(self.layout[row])):
    #             x = col * CELL_SIZE
    #             y = row * CELL_SIZE
                
    #             if self.layout[row][col] == 1:
    #                 # 벽 생성
    #                 self.walls.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
    #             elif self.layout[row][col] == 2:
    #                 # 점 생성
    #                 self.dots.append(Dot(x, y))
    #             elif self.layout[row][col] == 3:
    #                 # 파워 펠릿 생성
    #                 self.power_pellets.append(PowerPellet(x, y))
    
    # def draw(self, screen):
    #     """미로 그리기"""
    #     # TODO: 벽, 점, 파워펠릿 그리기
    #     # 벽 그리기
    #     for wall in self.walls:
    #         pygame.draw.rect(screen, BLUE, wall)
        
    #     # 점 그리기
    #     for dot in self.dots:
    #         dot.draw(screen)
        
    #     # 파워 펠릿 그리기
    #     for pellet in self.power_pellets:
    #         pellet.draw(screen)
    
    # def is_wall(self, x, y):
    #     """주어진 위치가 벽인지 확인"""
    #     # TODO: 충돌 검사 구현
    #     pass