"""
팩맨 게임 개발 대회 - 스크래치 코드
===================================

이 코드는 팩맨 게임의 기본 구조를 제공합니다.
참가자는 이 코드를 참고하여 객체지향 프로그래밍 원칙에 따라
완전한 팩맨 게임을 구현해야 합니다.

주요 구현 과제:
1. 각 클래스의 빈 메서드들을 구현
2. 게임 로직 완성
3. 충돌 감지 구현
4. 점수 시스템 구현
5. 게임 오버 및 승리 조건 구현
6. 창의적인 요소 추가 (가산점)

필수 요구사항:
- 객체지향 프로그래밍 원칙 준수
- 최소 500줄 이상의 코드
- 모든 핵심 기능 구현
"""

import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

# 게임 설정 상수
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CELL_SIZE = 20

# 색상 정의
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)


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


class Pacman(MovableObject):
    """팩맨 클래스"""
    
    def __init__(self, x, y):
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


class Ghost(MovableObject):
    """유령 기본 클래스"""
    
    def __init__(self, x, y, color, name):
        super().__init__(x, y, speed=1)
        self.color = color
        self.name = name
        self.is_frightened = False
        self.is_eaten = False
        self.home_x = x
        self.home_y = y
    
    def update(self):
        """유령 상태 업데이트"""
        # TODO: 유령의 이동 AI 구현
        pass
    
    def draw(self, screen):
        """유령 그리기"""
        # TODO: 유령을 화면에 그리기
        color = BLUE if self.is_frightened else self.color
        pygame.draw.rect(screen, color, self.rect)
    
    def chase_pacman(self, pacman):
        """팩맨 추적 AI"""
        # TODO: 팩맨을 추적하는 알고리즘 구현
        pass
    
    def flee_from_pacman(self, pacman):
        """팩맨으로부터 도망가는 AI"""
        # TODO: 팩맨으로부터 도망가는 알고리즘 구현
        pass


class Blinky(Ghost):
    """빨간 유령 - 직접 추적"""
    def __init__(self, x, y):
        super().__init__(x, y, RED, "Blinky")
    
    # TODO: Blinky만의 특별한 추적 패턴 구현


class Pinky(Ghost):
    """분홍 유령 - 앞쪽 차단"""
    def __init__(self, x, y):
        super().__init__(x, y, PINK, "Pinky")
    
    # TODO: Pinky만의 특별한 추적 패턴 구현


class Inky(Ghost):
    """하늘색 유령 - 예측 불가"""
    def __init__(self, x, y):
        super().__init__(x, y, CYAN, "Inky")
    
    # TODO: Inky만의 특별한 추적 패턴 구현


class Clyde(Ghost):
    """주황 유령 - 소심함"""
    def __init__(self, x, y):
        super().__init__(x, y, ORANGE, "Clyde")
    
    # TODO: Clyde만의 특별한 추적 패턴 구현


class Dot(GameObject):
    """일반 점"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.points = 10
        self.is_eaten = False
    
    def update(self):
        pass
    
    def draw(self, screen):
        """점 그리기"""
        if not self.is_eaten:
            pygame.draw.circle(screen, WHITE,
                             (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2),
                             3)


class PowerPellet(Dot):
    """파워 펠릿 (큰 점)"""
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.points = 50
    
    def draw(self, screen):
        """파워 펠릿 그리기"""
        if not self.is_eaten:
            pygame.draw.circle(screen, WHITE,
                             (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2),
                             6)


class Maze:
    """미로 클래스"""
    
    def __init__(self):
        # 미로 레이아웃 (1: 벽, 0: 빈 공간, 2: 점, 3: 파워 펠릿)
        self.layout = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
            [1,3,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,3,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
            [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
            [1,1,1,1,2,1,1,1,0,1,1,0,1,1,1,2,1,1,1,1],
            [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
            [1,1,1,1,2,1,0,1,1,0,0,1,1,0,1,2,1,1,1,1],
            [0,0,0,0,2,0,0,1,0,0,0,0,1,0,0,2,0,0,0,0],
            [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
            [0,0,0,1,2,1,0,0,0,0,0,0,0,0,1,2,1,0,0,0],
            [1,1,1,1,2,1,0,1,1,1,1,1,1,0,1,2,1,1,1,1],
            [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
            [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
            [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
            [1,1,2,1,2,1,2,1,1,1,1,1,1,2,1,2,1,2,1,1],
            [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
            [1,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,1],
            [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.dots = []
        self.power_pellets = []
        self.walls = []
        self.load_maze()
    
    def load_maze(self):
        """미로 데이터 로드"""
        # TODO: layout을 기반으로 벽, 점, 파워펠릿 객체 생성
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                x = col * CELL_SIZE
                y = row * CELL_SIZE
                
                if self.layout[row][col] == 1:
                    # 벽 생성
                    self.walls.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
                elif self.layout[row][col] == 2:
                    # 점 생성
                    self.dots.append(Dot(x, y))
                elif self.layout[row][col] == 3:
                    # 파워 펠릿 생성
                    self.power_pellets.append(PowerPellet(x, y))
    
    def draw(self, screen):
        """미로 그리기"""
        # TODO: 벽, 점, 파워펠릿 그리기
        # 벽 그리기
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)
        
        # 점 그리기
        for dot in self.dots:
            dot.draw(screen)
        
        # 파워 펠릿 그리기
        for pellet in self.power_pellets:
            pellet.draw(screen)
    
    def is_wall(self, x, y):
        """주어진 위치가 벽인지 확인"""
        # TODO: 충돌 검사 구현
        pass


class Game:
    """게임 메인 클래스"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("팩맨 게임")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.game_won = False
        
        # 게임 객체 초기화
        self.maze = Maze()
        self.pacman = Pacman(CELL_SIZE * 10, CELL_SIZE * 15)
        self.ghosts = [
            Blinky(CELL_SIZE * 10, CELL_SIZE * 9),
            Pinky(CELL_SIZE * 9, CELL_SIZE * 9),
            Inky(CELL_SIZE * 10, CELL_SIZE * 10),
            Clyde(CELL_SIZE * 11, CELL_SIZE * 9)
        ]
        
        self.score = 0
        self.high_score = 0
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # TODO: 키보드 입력 처리 (방향키로 팩맨 제어)
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = Direction.RIGHT
    
    def update(self):
        """게임 상태 업데이트"""
        if not self.game_over and not self.game_won:
            # TODO: 게임 로직 업데이트
            # 1. 팩맨 업데이트
            # 2. 유령 업데이트
            # 3. 충돌 검사
            # 4. 점수 업데이트
            # 5. 게임 종료 조건 확인
            
            self.pacman.update()
            
            for ghost in self.ghosts:
                ghost.update()
            
            self.check_collisions()
            self.check_win_condition()
    
    def check_collisions(self):
        """충돌 검사"""
        # TODO: 팩맨과 점/파워펠릿 충돌
        # TODO: 팩맨과 유령 충돌
        pass
    
    def check_win_condition(self):
        """승리 조건 확인"""
        # TODO: 모든 점을 먹었는지 확인
        pass
    
    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)
        
        # TODO: 모든 게임 객체 그리기
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)
        
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # TODO: 점수, 생명 등 UI 그리기
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """UI 요소 그리기"""
        # TODO: 점수, 생명, 게임 오버 메시지 등 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.game_won:
            win_text = font.render("YOU WIN!", True, YELLOW)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
    
    def run(self):
        """게임 메인 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """프로그램 진입점"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


"""
구현 과제 체크리스트:
===================

필수 구현 사항:
□ MovableObject의 move() 메서드 구현
□ MovableObject의 can_move() 메서드 구현
□ Pacman의 update() 메서드 완성
□ Pacman의 eat_dot() 메서드 구현
□ Ghost의 chase_pacman() 메서드 구현
□ Ghost의 flee_from_pacman() 메서드 구현
□ 각 유령(Blinky, Pinky, Inky, Clyde)의 고유한 AI 패턴 구현
□ Maze의 is_wall() 메서드 구현
□ Game의 check_collisions() 메서드 구현
□ Game의 check_win_condition() 메서드 구현

코드 작성 팁:
- 객체 간의 상호작용을 명확히 정의하세요
- 각 클래스의 책임을 명확히 구분하세요
- 상속을 적절히 활용하여 코드 중복을 줄이세요
- 주석을 충분히 작성하여 코드의 가독성을 높이세요
- Git을 사용하여 버전 관리를 하면 가산점이 있습니다

행운을 빕니다!
"""