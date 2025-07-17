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
                self.update(maze, i, j, pacman)
            return 0, self
        self.tick += 1
        if self.tick >= self.speed:
            # 다음 이동 방향이 벽인지를 update에서 next_dir 변경하며 확인
            self.tick = 0
            if pacman.is_powered_up:
                self.flee_from_pacman(maze, i, j, pacman)
            else:
                self.update(maze, i, j, pacman)
        if self.tick != self.speed//2:
            return 0, self
        tmp = maze[i][j].pop(k)
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
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

            if 0 <= ni <= MAX_Y and 0 <= nj <= MAX_X and (len(map[ni][nj]) == 0 or (len(map[ni][nj]) > 1 or map[ni][nj][0] != 1)):
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
    
    def wakeup(self, maze, i, j, pacman):
        dis = abs(pacman.iy - i) + abs(pacman.ix - j)
        if dis <= 3:
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
            
    # TODO: Blinky만의 특별한 추적 패턴 구현


class Pinky(Ghost):
    """분홍 유령 - 최적 경로"""
    def __init__(self, y, x, color, name):
        super().__init__(x, y, PINK, "Pinky")
        self.speed = 40
    
    def wakeup(self, maze, i, j, pacman):
        dis = abs(pacman.iy - i) + abs(pacman.ix - j)
        if dis <= 3:
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
        self.direction = Direction.NONE
    
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
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    i += 1
            elif (i > pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    i -= 1
        if (i == pacman.iy):
            if (j < pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    j += 1
            elif (j > pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
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
        if (i < pacman.iy):
            self.direction = Direction.DOWN
        if (j > pacman.ix):
            self.direction = Direction.LEFT
        if (j < pacman.ix):
            self.direction = Direction.RIGHT
    
    # TODO: Inky만의 특별한 추적 패턴 구현


class Clyde(Ghost):
    """주황 유령 - 경로 추적"""
    def __init__(self, y, x, color, name):
        super().__init__(x, y, ORANGE, "Clyde")
        self.path = []
        self.speed = 32
    
    def wakeup(self, maze, i, j, pacman):
        if (i != pacman.iy and j != pacman.ix):
            return False
        if (j == pacman.ix):
            if (i < pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    i += 1
            elif (i > pacman.iy):
                while (i != pacman.iy):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    i -= 1
        if (i == pacman.iy):
            if (j < pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    j += 1
            elif (j > pacman.ix):
                while (j != pacman.ix):
                    if len(maze[i][j]) > 0 and maze[i][j][0] == 1:
                        return False
                    j -= 1
        return True

    def update(self, maze, i, j, pacman):
        if len(self.path) == 0 or (self.path[-1][0] != pacman.iy or self.path[-1][1] != pacman.ix):
            self.path.append([pacman.iy, pacman.ix])
        if self.path[0][0] == i and self.path[0][1] == j:
            self.path.pop(0)
        if self.path[0][0] != i and self.path[0][1] != j:
            self.path.pop(0)
        if len(self.path) == 0:
            return
        if self.path[0][0] == i:
            if self.path[0][1] > j:
                self.direction = Direction.RIGHT
                return
            elif self.path[0][1] < j:
                self.direction = Direction.LEFT
                return
        if self.path[0][1] == j:
            if self.path[0][0] > i:
                self.direction = Direction.DOWN
                return
            elif self.path[0][0] < i:
                self.direction = Direction.UP
                return
        self.direction = Direction.NONE
    
    def flee_from_pacman(self, maze, i, j, pacman):
        self.update(maze, i, j, pacman)
        if len(self.path) == 0 or (self.path[0][0] != i or self.path[0][1] != j):
            self.path.insert(0,[i,j])
        super().flee_from_pacman(maze, i, j, pacman)
    
    # TODO: Clyde만의 특별한 추적 패턴 구현