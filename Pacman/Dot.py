import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Object import *

from Constants import *

class Dot(GameObject):
    """일반 점"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.points = 1
        self.is_eaten = False
    
    def update(self):
        pass
    
    def draw(self, screen, i, j, ygap, xgap):   # index 기반으로 출력
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
        self.points = 3
    
    def draw(self, screen, i, j, ygap, xgap):   # index 기반으로 출력
        """파워 펠릿 그리기"""
        self.x = j*CELL_SIZE + xgap
        self.y = i*CELL_SIZE + ygap
        if not self.is_eaten:
            pygame.draw.circle(screen, WHITE,
                             (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2),
                             6)