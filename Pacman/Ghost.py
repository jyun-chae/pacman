import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Object import *
from Pacman import *

from Constants import *

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
        
        self.direction = Direction.NONE
    
    @abstractmethod
    def update(self, maze, i, j, pacman):
        """유령 상태 업데이트"""
        # TODO: 유령의 이동 AI 구현
        # pacman이 power 상태면 flee~ 실행
        pass
    
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
    
    @abstractmethod
    def wakeup(self, maze, i, j, pacman):
        pass
    
    """앵간해서는 Object에서 처리하려고 했는데 너무 달라서 그냥 따로 처리 -> 기획실수 맞음 ㅇㅇ;;"""
    def move(self, maze, i, j, k, pacman):
        if self.direction == Direction.NONE:
            self.wakeup(maze, i, j, pacman.iy, pacman.ix)
            return 0
        self.tick += 1
        if self.tick >= self.speed:
            # 다음 이동 방향이 벽인지를 update에서 next_dir 변경하며 확인
            self.tick = 0
            self.update(maze, i, j, pacman.iy, pacman.ix)
        if self.tick != self.speed//2:
            return 0
        tmp = maze[i][j].pop(k)
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
        if i > MAX_Y or j > MAX_X:
            return 1
        if i < 0 or j < 0:
            return 1
        maze[i][j].append(tmp)
        return 0
    
    def flee_from_pacman(self, maze, i, j, pacman):
        """팩맨으로부터 도망가는 AI"""
        # TODO: 팩맨으로부터 도망가는 알고리즘 구현
        to_p = [pacman.iy - i, pacman.ix - j]
        if to_p[0] > 0 and to_p[1] > 0:
            if maze[i][j-1][0] != 1:
                self.direction = Direction.LEFT
                return
            if maze[i-1][j][0] != 1:
                self.direction = Direction.UP
                return
        elif to_p[0] > 0 and to_p[1] < 0:
            if maze[i][j+1][0] != 1:
                self.direction = Direction.RIGHT
                return
            if maze[i-1][j][0] != 1:
                self.direction = Direction.UP
                return
        elif to_p[0] < 0 and to_p[1] > 0:
            if maze[i][j-1][0] != 1:
                self.direction = Direction.LEFT
                return
            if maze[i+1][j][0] != 1:
                self.direction = Direction.DOWN
                return
        elif to_p[0] < 0 and to_p[1] < 0:
            if maze[i][j+1][0] != 1:
                self.direction = Direction.RIGHT
                return
            if maze[i+1][j][0] != 1:
                self.direction = Direction.DOWN
                return


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
    """하늘색 유령 - 직진"""
    def __init__(self, x, y):
        super().__init__(x, y, CYAN, "Inky")
        self.speed = 10
        
    def wakeup(self, maze, i, j, pacman):
        if (i != pacman.iy and j != pacman.ix):
            return False
        if (i == pacman.iy):
            while (i != pacman.iy):
                if maze[i][j][0] == 1:
                    return False
                i += 1
        if (j == pacman.ix):
            while (j != pacman.ix):
                if maze[i][j][0] == 1:
                    return False
                j += 1
        return True

    def update(self, maze, i, j, pacman):
        if (i > pacman.iy):
            self.direction = Direction.UP
        if (i < pacman.iy):
            self.direction = Direction.DOWN
        if (j > pacman.ix):
            self.direction = Direction.RIGHT
        if (j < pacman.ix):
            self.direction = Direction.LEFT
    
    # TODO: Inky만의 특별한 추적 패턴 구현


class Clyde(Ghost):
    """주황 유령 - 소심함"""
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, "Clyde")
    
    # TODO: Clyde만의 특별한 추적 패턴 구현