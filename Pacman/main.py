import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Object import *
from Pacman import *
from Ghost import *
from Dot import *
from Maze import *

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
        self.maze.draw(self.screen, -10, -10)
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