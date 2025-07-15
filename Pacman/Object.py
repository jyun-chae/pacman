import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

# 게임 설정 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

MAX_X = SCREEN_WIDTH//CELL_SIZE
MAX_Y = SCREEN_HEIGHT//CELL_SIZE

class Direction(Enum):
    """방향을 나타내는 열거형 클래스"""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    NONE = (0, 0)

class GameObject(ABC):
    """모든 게임 객체의 기본 클래스"""
    
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.rect = None
    
    @abstractmethod
    def update(self):
        """객체 상태 업데이트"""
        # 여기에 next_direction부분 옮김
        pass
    
    @abstractmethod
    def draw(self, screen):
        """화면에 객체 그리기"""
        pass


class MovableObject(GameObject):
    """움직일 수 있는 객체의 기본 클래스"""
    # can move는 move안에 합침
    
    def __init__(self, y, x, speed):
        super().__init__(y, x)
        self.tick = 0    # 이동중인 tick수
        self.speed = speed
        self.direction = Direction.NONE
    
    def move(self, maze, i, j, k):
        # 구현 문제로 그냥 벽 넘어가면 삭제 -> 계속해서 움직이는 ghost는 -x, +y방향으로 먼저 움직이도록 지시
        """객체 이동 처리"""
        # TODO: 이동 로직 구현
        # 힌트: self.direction의 값에 따라 x, y 좌표 업데이트
        if self.direction == Direction.NONE:
            self.update(maze, i, j)
            return 0
        self.tick += 1
        if self.tick >= self.speed:
            # 다음 이동 방향이 벽인지를 update에서 next_dir 변경하며 확인
            self.tick = 0
            self.update(maze, i, j)
        if self.tick != self.speed//2:
            return 0
        tmp = maze[i][j].pop(k)
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
        if i > MAX_Y or j > MAX_X:
            # del maze[i][j][k]
            return 1
        if i < 0 or j < 0:
            # del maze[i][j][k]
            return 1
        maze[i][j].append(tmp)
        return 0