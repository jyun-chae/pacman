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

class Pacman(MovableObject):
    """팩맨 클래스"""
    
    def __init__(self, x, y, name = "pacman"):
        super().__init__(x, y, speed=2)
        self.lives = 3
        self.score = 0
        self.is_powered_up = False
        self.power_up_timer = 0
    
    def update(self):
        """팩맨 상태 업데이트"""
        # TODO: 팩맨의 이동, 파워업 타이머 등 업데이트
        pass
    
    def draw(self, screen):
        """팩맨 그리기"""
        # TODO: 팩맨을 화면에 그리기
        # 힌트: pygame.draw.circle() 또는 이미지 사용
        pygame.draw.circle(screen, YELLOW, 
                         (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2), 
                         CELL_SIZE//2 - 2)
    
    def eat_dot(self, dot):
        """점 먹기"""
        # TODO: 점수 증가 및 파워업 처리
        pass
    
    def lose_life(self):
        """생명 잃기"""
        # TODO: 생명 감소 처리
        pass