import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Constants import *

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
    
    def move(self, maze, i, j, k, pacman):
        """객체 이동 처리"""
        # TODO: 이동 로직 구현
        # 힌트: self.direction의 값에 따라 x, y 좌표 업데이트
        if self.direction == Direction.NONE:    # Direction.NONE 즉 새로 움직이는 경우 update해서 방향 파악
            self.update(maze, i, j)
            return 0
        self.tick += 1
        if self.tick >= self.speed: # 다음 칸으로 완벽히 넘어가서 새로운 방향 찾기
            self.tick = 0
            self.update(maze, i, j)
        if self.tick != self.speed//2:  # 아직 몸의 절반이 걸터져 있지 않으면 skip
            return 0
        tmp = maze[i][j].pop(k) # 과거의 나는 버린다
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
        if i > MAX_Y or j > MAX_X:
            # del maze[i][j][k]
            return 1
        if i < 0 or j < 0:
            # del maze[i][j][k]
            return 1
        maze[i][j].append(tmp)  # 새로운 나로 태어날 뿐
        return 0