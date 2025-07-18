import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod
from heapq import heappush, heappop

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
        self.x += CELL_SIZE//2
        self.y += CELL_SIZE//2
        pygame.draw.rect(screen, color, self.rect)
    
    @abstractmethod
    def wakeup(self, maze, i, j, pacman):
        pass
    
    """앵간해서는 Object에서 처리하려고 했는데 너무 달라서 그냥 따로 처리 -> 기획실수 맞음 ㅇㅇ;;"""
    def move(self, maze, i, j, k, pacman):
        self.i = i
        self.j = j
        if self.direction == Direction.NONE:
            if self.wakeup(maze, i, j, pacman):
                self.tick = 0
            else:
                return 0, self
        if self.tick >= self.speed:
            self.tick = 0
        if not self.tick:
            if pacman.is_powered_up:
                self.flee_from_pacman(maze, i, j, pacman)
            else:
                self.update(maze, i, j, pacman)
        self.tick += 1
        if type(self) == Blinky:
            if self.bob():
                return -1, self
        if self.tick != self.speed//2:
            return 0, self
        tmp = maze[i][j].pop(k)
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
        if len(maze[i][j]) and maze[i][j][0] == 1:
            raise Exception(f"{self}")
        if i > MAX_Y or j > MAX_X:
            return 1, self
        if i < 0 or j < 0:
            return 1, self
        maze[i][j].append(tmp)
        self.i = i
        self.j = j
        return 0, self
    
    def run_away(self, maze, i, j, dir):
        if len(maze[i + dir.value[0]][j + dir.value[1]]) == 0 or maze[i + dir.value[0]][j + dir.value[1]][0] != 1:
                self.direction = dir
                return 1
        return 0
    
    def flee_from_pacman(self, maze, i, j, pacman):
        """팩맨으로부터 도망가는 AI"""
        # TODO: 팩맨으로부터 도망가는 알고리즘 구현
        to_p = [pacman.iy - i, pacman.ix - j]
        if to_p[0] > 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] > 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] < 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        elif to_p[0] < 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        elif to_p[0] == 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
        elif to_p[0] == 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
        elif to_p[0] > 0 and to_p[1] == 0:
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] < 0 and to_p[1] == 0:
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        self.direction = Direction.NONE
    
    def last_hope(self, maze, i, j, pacman):
        """최적경로가 안찾아 질 때 최후의 보루"""
        # TODO: 팩맨으로부터 도망가는 알고리즘 구현
        to_p = [pacman.iy - i, pacman.ix - j]
        if to_p[0] < 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] < 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] > 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        elif to_p[0] > 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        elif to_p[0] == 0 and to_p[1] > 0:
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
        elif to_p[0] == 0 and to_p[1] < 0:
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
        elif to_p[0] > 0 and to_p[1] == 0:
            if self.run_away(maze, i, j, Direction.UP):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.DOWN):
                return
        elif to_p[0] < 0 and to_p[1] == 0:
            if self.run_away(maze, i, j, Direction.DOWN):
                return
            if self.run_away(maze, i, j, Direction.RIGHT):
                return
            if self.run_away(maze, i, j, Direction.LEFT):
                return
            if self.run_away(maze, i, j, Direction.UP):
                return
        self.direction = Direction.NONE

def heuristic(a, b):
    # 맨해튼 거리
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def A_star(map, i, j, pacman):
    start = (i, j)
    goal = (pacman.iy, pacman.ix)

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            # 경로 복원
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path[0] if path else start  # 현재 위치가 goal이면 그대로

        for dx, dy in directions:
            ni, nj = current[0] + dy, current[1] + dx

            if 0 <= ni <= MAX_Y and 0 <= nj <= MAX_X and (len(map[ni][nj]) == 0 or map[ni][nj][0] != 1):
                neighbor = (ni, nj)
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

    # 도달 불가능할 경우 원위치 반환
    return (i, j)

class Blinky(Ghost):
    """빨간 유령 - 자폭"""
    def __init__(self, y, x, color, name):
        super().__init__(y, x, RED, "Blinky")
        self.speed = 60
        self.life = 5*FPS/self.speed
    
    def wakeup(self, maze, i, j, pacman):
        dis = abs(pacman.iy - i) + abs(pacman.ix - j)
        if dis <= 5:
            return True
        return False

    def update(self, maze, i, j, pacman):
        self.life -= 1
        p_i, p_j = A_star(maze, i, j, pacman)
        if p_i == i:
            if p_j > j:
                self.direction = Direction.RIGHT
                return
            elif p_j < j:
                self.direction = Direction.LEFT
                return
        if p_j == j:
            if p_i > i:
                self.direction = Direction.DOWN
                return
            elif p_i < i:
                self.direction = Direction.UP
                return
        self.last_hope(maze, i, j, pacman)
            
    def bob(self):
        if self.life <= 0:
            return True
        return False
    # TODO: Blinky만의 특별한 추적 패턴 구현


class Pinky(Ghost):
    """분홍 유령 - 최적 경로"""
    def __init__(self, y, x, color, name):
        super().__init__(x, y, PINK, "Pinky")
        self.speed = 40
    
    def wakeup(self, maze, i, j, pacman):
        dis = abs(pacman.iy - i) + abs(pacman.ix - j)
        if dis <= 5:
            return True
        return False

    def update(self, maze, i, j, pacman):
        p_i, p_j = A_star(maze, i, j, pacman)
        if p_i == i:
            if p_j > j:
                self.direction = Direction.RIGHT
                return
            elif p_j < j:
                self.direction = Direction.LEFT
                return
        if p_j == j:
            if p_i > i:
                self.direction = Direction.DOWN
                return
            elif p_i < i:
                self.direction = Direction.UP
                return
        self.last_hope(maze, i, j, pacman)
    
    # TODO: Pinky만의 특별한 추적 패턴 구현


class Inky(Ghost):
    """하늘색 유령 - 직진"""
    def __init__(self, y, x, color, name):
        super().__init__(x, y, CYAN, "Inky")
        self.speed = 10
        
    def wakeup(self, maze, i, j, pacman):
        if (i != pacman.iy and j != pacman.ix):
            return False
        if (j == pacman.ix):
            if (i < pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    i += 1
            elif (i > pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    i -= 1
        if (i == pacman.iy):
            if (j < pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    j += 1
            elif (j > pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    j -= 1
        return True

    def update(self, maze, i, j, pacman):
        if len(maze[i+self.direction.value[0]][j+self.direction.value[1]]) and maze[i+self.direction.value[0]][j+self.direction.value[1]][0] == 1:
            self.direction = Direction.NONE
            return
        if self.direction != Direction.NONE:
            return
        if (i > pacman.iy):
            self.direction = Direction.UP
            return
        if (i < pacman.iy):
            self.direction = Direction.DOWN
            return
        if (j > pacman.ix):
            self.direction = Direction.LEFT
            return
        if (j < pacman.ix):
            self.direction = Direction.RIGHT
            return
        self.direction = Direction.NONE
    # TODO: Inky만의 특별한 추적 패턴 구현


class Clyde(Ghost):
    """주황 유령 - 경로 추적""""""용감해서 꽁무니를 쫓고, 도망가지 않음"""
    def __init__(self, y, x, color, name):
        super().__init__(x, y, ORANGE, "Clyde")
        self.speed = 32
        self.index = -1
        self.p_y = 0
        self.p_x = 0
    
    def wakeup(self, maze, i, j, pacman):
        if (pacman.is_powered_up):
            return
        if (i != pacman.iy and j != pacman.ix):
            return False
        if (j == pacman.ix):
            if (i < pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    i += 1
            elif (i > pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    i -= 1
        if (i == pacman.iy):
            if (j < pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    j += 1
            elif (j > pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) == 1 and maze[i][j][0] == 1:
                        return False
                    j -= 1
        return True

    def update(self, maze, i, j, pacman):
        if self.index == -1:
            self.index = pacman.index
            self.p_y = pacman.iy - i
            self.p_x = pacman.ix - j
            # if self.p_y:
            #     self.p_y += abs(self.p_y)/self.p_y
            # if self.p_x:
            #     self.p_x += abs(self.p_x)/self.p_x
            self.p_y = int(self.p_y)
            self.p_x = int(self.p_x)
        if self.p_y > 0:
            self.direction = Direction.DOWN
            self.p_y -= 1
            return
        if self.p_y < 0:
            self.direction = Direction.UP
            self.p_y += 1
            return
        if self.p_x > 0:
            self.direction = Direction.RIGHT
            self.p_x -= 1
            return
        if self.p_x < 0:
            self.direction = Direction.LEFT
            self.p_x += 1
            return
        self.index += 1
        if self.index > pacman.index:
            if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:
                self.direction = Direction.NONE
            return
        self.direction = pacman.path[self.index]
        if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:
            self.index += 1
            if self.index > pacman.index:
                if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:
                    self.direction = Direction.NONE
            else:
                self.direction = pacman.path[self.index]
                if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:
                    self.direction = Direction.NONE
        # self.index += 1
        return

    def flee_from_pacman(self, maze, i, j, pacman):
        self.index = -1
        self.direction = Direction.NONE
    
    # TODO: Clyde만의 특별한 추적 패턴 구현