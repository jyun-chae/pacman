import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Object import *

# 게임 설정 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

# 색상 정의
YELLOW = (255, 255, 0)

class Direction(Enum):
    """방향을 나타내는 열거형 클래스"""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    NONE = (0, 0)

class Pacman(MovableObject):
    """팩맨 클래스"""
    
    def __init__(self, y, x, color = YELLOW, name = "pacman"):
        super().__init__(y, x, speed=30)
        self.color = YELLOW
        self.ix = x
        self.iy = y
        self.next_dir = Direction.NONE
        self.lives = 3
        self.score = 0
        self.is_powered_up = False
        self.power_up_timer = 0
    
    def update(self, maze, i, j):
        """팩맨 상태 업데이트"""
        # TODO: 팩맨의 이동, 파워업 타이머 등 업데이트
        self.direction = self.next_dir
        i += self.direction.value[0]
        j += self.direction.value[1]
        if maze[i][j][0] == 1:
            self.direction = Direction.NONE
        return
    
    def draw(self, screen, i, j, ygap, xgap):
        """팩맨 그리기"""
        # TODO: 팩맨을 화면에 그리기
        # 힌트: pygame.draw.circle() 또는 이미지 사용
        if (self.tick < self.speed/2):
            self.x = j*CELL_SIZE + CELL_SIZE//2 + xgap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + CELL_SIZE//2 + ygap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[0]
        else:
            self.x = j*CELL_SIZE + CELL_SIZE//2 + xgap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + CELL_SIZE//2 + ygap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[0]
        pygame.draw.circle(screen, self.color, (self.x, self.y), CELL_SIZE//2 - 2)
    
    def eat_dot(self, dot):
        """점 먹기"""
        # TODO: 점수 증가 및 파워업 처리
        pass
    
    def lose_life(self):
        """생명 잃기"""
        # TODO: 생명 감소 처리
        pass
    
    def cmd_input(self, dir):
        self.next_dir = dir