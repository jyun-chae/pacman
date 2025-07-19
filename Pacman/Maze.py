import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod
from copy import deepcopy
import random as rd

from Dot import *
from Ghost import *
from Pacman import *
from Object import *

from Constants import *

# maze안에 들어가는 object 종류 -> dot들은 그냥 2, 3 int형으로 저장
OBJECTS = [[Pacman, YELLOW, "pacman"],
           [Blinky, RED, "bomb"],
           [Pinky, PINK, "chase"],
           [Inky, CYAN, "dash"],
           [Clyde, ORANGE, "follow"]
           ]

class Maze:
    """미로 클래스"""
    def __init__(self):
        self.row = 0
        self.col = 0
        self.maze = []
        self.tot_maze = []  # 화면에 나오는 maze의 list 3차원 [y index][x index][해당 칸의 object, 벽, 점 등 값들]
        
        # 어쩔수 없이 들어가는 pacman 초기위치값
        self.p_y = 0
        self.p_x = 0
        
        # 지금까지 화면이 밀린 index들
        self.y_idx = 0
        self.x_idx = 0
        # 맵 정보 읽기
        self.read_txt('./datas/map.txt')
        self.make_tot_map(0)
    
    def read_txt(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            self.row, self.col = map(int, lines[0].split())
            
            for line in lines[1:1+self.row]:
                self.maze.append(list(map(int, line.split())))
            
            for i in range(self.row):   # txt의 특정 줄에서 입력값에 맞지 않는 개수가 있는 경우
                if self.col != len(self.maze[i]):
                    raise Exception("map.txt의 구조에 문제가 있습니다")
            
            for i in range(self.row):
                for j in range(self.col):
                    if self.maze[i][j] < 0 or self.maze[i][j] > 8:  # 범위 밖의 수가 들어간 경우
                        raise Exception("map.txt의 구조에 문제가 있습니다")
                    if self.maze[i][j] == 4:    # 팩맨은 단 1개만 존재해야 하므로 따로 저장
                        self.p_y = i
                        self.p_x = j
                        self.maze[i][j] = [0]
                    else:
                        self.maze[i][j] = [self.maze[i][j]]
                    if self.maze[i][j][0] > 3:  # 유령및 팩맨의 위치의 첫번째 index값은 0이다
                        self.maze[i][j].insert(0,0)
            
            if self.p_y > MAX_Y or self.p_x > MAX_X:    # 화면이 너무 작은 경우
                raise Exception("초기 팩맨의 위치가 이상합니다")
        except Exception as e:
            raise Exception(e)  # 오류 메세지와 함께 출력 -> 자잘한 실수만 따로 적어놯지 숫자가 아닌거를 넣는다거나 같은 이상한건 따로 처리 안함 ㅅㄱ
    # 초기 화면 및 tot_maze 구성
    def make_tot_map(self, level):
        x_cnt = 0
        y_cnt = 0
        while (y_cnt <= MAX_Y):
            x_cnt = 0
            self.tot_maze.append([])
            while (x_cnt <= MAX_X):
                self.tot_maze[y_cnt].append(self.maze[y_cnt%self.row][x_cnt%self.col].copy())   # 맨 처음 읽은 maze를 기반으로 복사해서 사용
                x_cnt += 1
            y_cnt += 1
        
        # 맵에 객체 추가
        for i in range(MAX_Y+1):
            for j in range(MAX_X+1):
                if len(self.tot_maze[i][j]) > 1:
                    tmp = self.tot_maze[i][j][1]
                    proba = rd.randint(1,10)
                    if proba > LEVELS[level]:   # 초기 level 즉 0에 해당하는 확률로 ghost 생성 안함
                        self.tot_maze[i][j].pop(1)
                    else:
                        self.tot_maze[i][j][1] = OBJECTS[tmp - 4][0](i, j, OBJECTS[tmp - 4][1], OBJECTS[tmp - 4][2])    # 생성하기로 결정한 경우
        
        self.tot_maze[self.p_y][self.p_x] = [Pacman(self.p_y, self.p_x)]
    
    # 모든 tot_maze를 x축으로 1칸 이동
    def shift_map_x(self, level):
        level = min(4, level)   # level = time이기 때문에 40초를 초과하는 경우 그냥 40초때의 값으로 진행
        self.x_idx += 1
        for i in range(MAX_X):
            for j in range(MAX_Y+1):
                self.tot_maze[j][i] = deepcopy(self.tot_maze[j][i+1])   # tot_maze부터는 object가 존재 -> deepcopy진행
        y_cnt = 0
        while (y_cnt <= MAX_Y): # 맨 마지막 줄을 maze에서 해당 부분을 파악후 가져옴
            self.tot_maze[y_cnt][MAX_X] = deepcopy(self.maze[(self.y_idx + y_cnt)%self.row][(self.x_idx + MAX_X)%self.col])
            y_cnt += 1
        for i in range(MAX_Y+1):
            if len(self.tot_maze[i][MAX_X]) > 1:
                tmp = self.tot_maze[i][MAX_X][1]
                proba = rd.randint(1,10)    # 추가된 부분을 현제 level에 맞는 확률로 추가
                if proba > LEVELS[level]:
                    self.tot_maze[i][MAX_X].pop(1)
                else:
                    self.tot_maze[i][MAX_X][1] = OBJECTS[tmp - 4][0](0, 0, OBJECTS[tmp - 4][1], OBJECTS[tmp - 4][2])   # 위치 나중에 수정
    # 모든 tot_maze를 y축으로 1칸 이동 이하동문        
    def shift_map_y(self, level):
        level = min(4, level)
        self.y_idx += 1
        for i in range(MAX_Y):
            self.tot_maze[i][:] = deepcopy(self.tot_maze[i+1][:])
        x_cnt = 0
        while (x_cnt <= MAX_X):
            self.tot_maze[MAX_Y][x_cnt] = deepcopy(self.maze[(self.y_idx + MAX_Y)%self.row][(self.x_idx + x_cnt)%self.col])
            x_cnt += 1
        for j in range(MAX_X+1):
            if len(self.tot_maze[MAX_Y][j]) > 1:
                # 나중에 상세값 수정
                tmp = self.tot_maze[MAX_Y][j][1]
                proba = rd.randint(1,10)
                if proba > LEVELS[level]:
                    self.tot_maze[MAX_Y][j].pop(1)
                else:
                    self.tot_maze[MAX_Y][j][1] = OBJECTS[tmp - 4][0](0, 0, OBJECTS[tmp - 4][1], OBJECTS[tmp - 4][2])   # 위치 나중에 수정
    
    def draw(self, screen, ygap, xgap):
        x_cnt = 0
        y_cnt = 0
        # ygap, xgap에 맞추어 벽 출력
        while (y_cnt <= MAX_Y):
            x_cnt = 0
            while (x_cnt <= MAX_X):
                if self.maze[(self.y_idx + y_cnt)%self.row][(self.x_idx + x_cnt)%self.col] == [1]:
                    pygame.draw.rect(screen, BLUE, pygame.Rect(x_cnt*CELL_SIZE + xgap, y_cnt*CELL_SIZE + ygap, CELL_SIZE, CELL_SIZE))
                x_cnt += 1
            y_cnt += 1