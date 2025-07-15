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
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Ghost(MovableObject):
    """유령 기본 클래스"""
    
    def __init__(self, y, x, color, name):
        super().__init__(y, x, speed=30)
        self.color = color
        self.name = name
        self.is_frightened = False
        self.is_eaten = False
        self.home_x = x
        self.home_y = y
        
        self.sleep = True
    
    def update(self, maze, i, j):
        """유령 상태 업데이트"""
        # TODO: 유령의 이동 AI 구현
        if self.sleep:
            return
    
    def draw(self, screen, i, j, ygap, xgap):
        """유령 그리기"""
        # TODO: 유령을 화면에 그리기
        color = BLUE if self.is_frightened else self.color
        if (self.tick < self.speed/2):
            self.x = j*CELL_SIZE + xgap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + ygap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[0]
        else:
            self.x = j*CELL_SIZE + xgap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + ygap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[0]
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, color, self.rect)
    
    def chase_pacman(self, pacman):
        """팩맨 추적 AI"""
        # TODO: 팩맨을 추적하는 알고리즘 구현
        pass
    
    def flee_from_pacman(self, pacman):
        """팩맨으로부터 도망가는 AI"""
        # TODO: 팩맨으로부터 도망가는 알고리즘 구현
        pass


class Blinky(Ghost):
    """빨간 유령 - 직접 추적"""
    def __init__(self, y, x, color, name):
        super().__init__(y, x, color, name)
    
    # TODO: Blinky만의 특별한 추적 패턴 구현


class Pinky(Ghost):
    """분홍 유령 - 앞쪽 차단"""
    def __init__(self, x, y):
        super().__init__(x, y, PINK, "Pinky")
    
    # TODO: Pinky만의 특별한 추적 패턴 구현


class Inky(Ghost):
    """하늘색 유령 - 예측 불가"""
    def __init__(self, x, y):
        super().__init__(x, y, CYAN, "Inky")
    
    # TODO: Inky만의 특별한 추적 패턴 구현


class Clyde(Ghost):
    """주황 유령 - 소심함"""
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, "Clyde")
    
    # TODO: Clyde만의 특별한 추적 패턴 구현