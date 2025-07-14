import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

# 게임 설정 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

class Direction(Enum):
    """방향을 나타내는 열거형 클래스"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

class GameObject(ABC):
    """모든 게임 객체의 기본 클래스"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    
    @abstractmethod
    def update(self):
        """객체 상태 업데이트"""
        pass
    
    @abstractmethod
    def draw(self, screen):
        """화면에 객체 그리기"""
        pass


class MovableObject(GameObject):
    """움직일 수 있는 객체의 기본 클래스"""
    
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.speed = speed
        self.direction = Direction.NONE
        self.next_direction = Direction.NONE
    
    def move(self):
        """객체 이동 처리"""
        # TODO: 이동 로직 구현
        # 힌트: self.direction의 값에 따라 x, y 좌표 업데이트
        pass
    
    def can_move(self, direction, maze):
        """주어진 방향으로 이동 가능한지 확인"""
        # TODO: 미로와의 충돌 검사 구현
        # 힌트: 다음 위치가 벽인지 확인
        pass