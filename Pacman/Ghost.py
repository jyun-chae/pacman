'''
할말이 많아서 여기에 적습니다
일단 기존의 팩맨은 유령의 ai가 최적경로 탐색도 아니고, 
유령별 차이점이 현재 팩맨 위치 쫓는 얘, 팩맨이 바라보는 4칸 앞 쫓는 얘, 무슨 이상한 쓸대없는 위치 쫓는 얘, 와리가리 치는 얘 이렇게 있습니다.
이를 보고는 정말 개성 없고 예측 불가능한 유령이 많다고 판단했습니다. 
이에 자폭병, 최적경로로 쫓는 아이, 뒤를 졸졸 따라오는 아이, 무지성 박치기(모티브 받음) 이렇게 4가지로 구성했습니다. 
또한, 최적경로이기도 하고, 무한정 넓어지는 맵에서 처음부터 태어난 유령이 쫓아오는 것은 불합리하다고 생각해서 수면(모티브 받음) 패턴을 도입했습니다
자폭병의 경우 최적경로로 가기에 매커니즘이 비슷하지만 느린 속도로 다가오는 큰 위협이기에 충분히 개성있다고 생각했습니다
모든 객체의 속도는 이러합니다 자폭병 < 최적경로 < 따라쟁이 ~~ 팩맨 < 돌진
모티브 받음 게임과의 차이점은 맵에서의 변화와 유령의 능력 종류, 무적 상태일때 도망가는 패턴이 있다는 점, 시간이 지날수록 ghost 생성 확률이 달라진다는 점, 수면에서 일어나는 방법에 다양함이 있다는 점 등 차이점이 많습니다
'''

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
    
    def draw(self, screen, i, j, ygap, xgap):   # 출력은 self.tick과 self.speed의 비율을 기반으로 진행
        """유령 그리기"""
        # TODO: 유령을 화면에 그리기
        color = BLUE if self.is_frightened else self.color
        if (self.tick < self.speed/2):  # 아직 넘어가기 전
            self.x = j*CELL_SIZE + xgap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + ygap + (self.tick/self.speed)*CELL_SIZE*self.direction.value[0]
        else:   # 넘어간 후
            self.x = j*CELL_SIZE + xgap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[1]
            self.y = i*CELL_SIZE + ygap - ((self.speed - self.tick)/self.speed)*CELL_SIZE*self.direction.value[0]
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        self.x += CELL_SIZE//2
        self.y += CELL_SIZE//2
        pygame.draw.rect(screen, color, self.rect)
    
    @abstractmethod
    def wakeup(self, maze, i, j, pacman):   # 자고있는 유령을 깨울지 판단
        pass
    
    """앵간해서는 Object에서 처리하려고 했는데 너무 달라서 그냥 따로 처리 -> 기획실수 맞음 ㅇㅇ;;"""
    def move(self, maze, i, j, k, pacman):
        self.i = i
        self.j = j
        if self.direction == Direction.NONE:    # 자니? 일어나
            if self.wakeup(maze, i, j, pacman):
                self.tick = 0   # 일어났구나 오태식이
            else:
                return 0, self  # 그냥 쳐 자
        if self.tick >= self.speed:
            self.tick = 0
        if not self.tick:   # 일어났거나 완전히 이동한 뒤
            if pacman.is_powered_up:    # 도망가야 하는가?
                self.flee_from_pacman(maze, i, j, pacman)
            else:   # 그냥 길찾자
                self.update(maze, i, j, pacman)
        self.tick += 1
        if type(self) == Blinky:    # 폭탄병이면 자기 터지는지 확인
            if self.bob():
                return -1, self
        if self.tick != self.speed//2:  # 이동 여부 확인
            return 0, self
        tmp = maze[i][j].pop(k) # 과거의 나는 없다
        i += self.direction.value[0]
        j += self.direction.value[1]
        # canmove의 부분 범위 밖이면 삭제
        if i > MAX_Y or j > MAX_X or i < 0 or j < 0:
            return 1, self
        if maze[i][j] == [1]:   # 하도 버그 많이나서 넣어놈 만약 버그 나면 연락주세요 연락처는 010-1234-5678
            raise Exception(f"{self}")
        maze[i][j].append(tmp)  # 새로운 나만 있을뿐
        self.i = i
        self.j = j
        return 0, self
    
    def run_away(self, maze, i, j, dir):    # 함수명은 이런데 실상은 해당 방향으로 이동했을때 갈 수 있는지 확인하는 놈
        i += dir.value[0]
        j += dir.value[1]
        if i > MAX_Y or j > MAX_X or i < 0 or j < 0:    # 죽어버림
            return 0
        if maze[i][j] != [1]:   # 벽이 아니면 허가
                self.direction = dir
                return 1
        return 0
    
    def flee_from_pacman(self, maze, i, j, pacman): # 돔황챠 : 모든 도망치는 방향은 일단 팩맨에서 도망치면서 x축 이동을 우선순위를 두고 같은 방향끼리는 y+, x+를 우선순위로 둠
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
    
    def last_hope(self, maze, i, j, pacman):    # 가끔 A*알고리즘이 작동하지 않는 경우가 있어서 그때를 위한 최후의 보루 우선순위는 flee와 다 똑같은데 가장 먼저 가까워지는걸 우선한다는 것 정도
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

def A_star(map, i, j, pacman):  # 딴건 다 내가 짰는데 이거는 gpt 시킴 map이 워낙 넓어서 길찾기 잘못돌리면 터질거 같아서 물어봄
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

class Blinky(Ghost):    # 일명 폭탄병
    """빨간 유령 - 자폭"""
    def __init__(self, y, x, color, name):
        super().__init__(y, x, RED, "Blinky")
        self.speed = 60
        self.life = 5*FPS/self.speed
    
    def wakeup(self, maze, i, j, pacman):   # 맨해튼거리로 5칸 이내 들어오면 일어남
        dis = abs(pacman.iy - i) + abs(pacman.ix - j)
        if dis <= 5:
            return True
        return False

    def update(self, maze, i, j, pacman):
        if self.direction != Direction.NONE:
            self.life -= 1  # 째깍째깍
        p_i, p_j = A_star(maze, i, j, pacman)   # 길찾기
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
        self.last_hope(maze, i, j, pacman)  # 이걸 못찾네;;
            
    def bob(self):  # 펑!
        if self.life <= 0:
            return True
        return False
    # TODO: Blinky만의 특별한 추적 패턴 구현


class Pinky(Ghost): # 터지는거 배고 폭탄병과 동일
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
        
    def wakeup(self, maze, i, j, pacman):   # 자기 기준 십자 안에 보이면 일어남
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

    def update(self, maze, i, j, pacman):   # 처음 봤던 팩맨 위치로 계속 이동
        if i+self.direction.value[0] > MAX_Y or j+self.direction.value[1] > MAX_X or i+self.direction.value[0] < 0 or j+self.direction.value[1] < 0:
            return
        if maze[i+self.direction.value[0]][j+self.direction.value[1]] == [1]:
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
        self.index = -1 # 팩맨의 경로에서 내가 따라가고 있는 index값
        self.p_y = 0
        self.p_x = 0
    
    def wakeup(self, maze, i, j, pacman):   # 십자 안에 보이면 일어남
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
        if self.index == -1:    # 갓 일어난 아이
            self.index = pacman.index
            self.p_y = int(pacman.iy - i)
            self.p_x = int(pacman.ix - j)
        # 처음 봤던 팩맨까지 무지성 이동 -> 봤다 == 그 사이에 벽이 없다는 것을 의미하기 때문
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
        if self.index > pacman.index:   # 거의 다 따라잡은 경우 pacman 바로 뒤에 있으면 index out of range 일어남
            if i+self.direction.value[0] > MAX_Y or j+self.direction.value[1] > MAX_X or i+self.direction.value[0] < 0 or j+self.direction.value[1] < 0:
                self.direction = Direction.NONE
                return
            if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:
                self.direction = Direction.NONE
            return
        self.direction = pacman.path[self.index]    # pacman의 path를 통해 따라감
        if i+self.direction.value[0] > MAX_Y or j+self.direction.value[1] > MAX_X or i+self.direction.value[0] < 0 or j+self.direction.value[1] < 0:
                self.direction = Direction.NONE
                return
        if maze[i + self.direction.value[0]][j + self.direction.value[1]] == [1]:   # 가끔 도망가고 다시 따라가는 과정에서 오류 생기는 일이 있어서 추가
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

    def flee_from_pacman(self, maze, i, j, pacman): # 난 쫄지 않아 도망가지 않음
        self.index = -1
        self.direction = Direction.NONE
    
    # TODO: Clyde만의 특별한 추적 패턴 구현