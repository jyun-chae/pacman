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
WHITE = (255, 255, 255)

class Dot(GameObject):
    """일반 점"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.points = 1
        self.is_eaten = False
    
    def update(self):
        pass
    
    def draw(self, screen, i, j, ygap, xgap):
        """점 그리기"""
        self.x = j*CELL_SIZE + xgap
        self.y = i*CELL_SIZE + ygap
        if not self.is_eaten:
            pygame.draw.circle(screen, WHITE,
                             (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2),
                             3)


class PowerPellet(Dot):
    """파워 펠릿 (큰 점)"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.points = 50
    
    def draw(self, screen, i, j, ygap, xgap):
        """파워 펠릿 그리기"""
        self.x = j*CELL_SIZE + xgap
        self.y = i*CELL_SIZE + ygap
        if not self.is_eaten:
            pygame.draw.circle(screen, WHITE,
                             (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2),
                             6)