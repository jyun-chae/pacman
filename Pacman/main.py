import pygame
import sys
from enum import Enum
from abc import ABC, abstractmethod

from Constants import *

from Object import *
from Pacman import *
from Ghost import *
from Dot import *
from Maze import *

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
        self.pacman = self.maze.tot_maze[self.maze.p_y][self.maze.p_x][0]
        self.ghosts = [
            Blinky,
            Pinky,
            Inky,
            Clyde
        ]
        self.dots = Dot(0,0)
        self.power_dots = PowerPellet(0,0)
        
        self.score = 0
        self.high_score = 0
        
        self.ygap = -10
        self.xgap = -10
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # TODO: 키보드 입력 처리 (방향키로 팩맨 제어)
                if event.key == pygame.K_UP:
                    self.pacman.cmd_input(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.pacman.cmd_input(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.pacman.cmd_input(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.cmd_input(Direction.RIGHT)
    
    def update(self):
        """게임 상태 업데이트"""
        if not self.game_over and not self.game_won:
            # TODO: 게임 로직 업데이트
            # 1. 팩맨 업데이트
            # 2. 유령 업데이트
            # 3. 충돌 검사
            # 4. 점수 업데이트
            # 5. 게임 종료 조건 확인
            
            tot_maze = self.maze.tot_maze
            
            for i in range(MAX_Y + 1):
                for j in range(MAX_X + 1):
                    isthere = [0,0,0,0] # 팩맨, 유령, 점, 파워점
                    if len(tot_maze[i][j]) == 1 and type(tot_maze[i][j][0]) == int:
                        continue
                    k = 0
                    while (k < len(tot_maze[i][j])):
                        tmp = 0
                        if type(tot_maze[i][j][k]) == Pacman:
                            self.pacman = tot_maze[i][j][k]
                            isthere[0] = 1
                            tmp = tot_maze[i][j][k].move(tot_maze, i ,j, k)
                        elif type(tot_maze[i][j][k]) in self.ghosts:
                            isthere[1] = 1
                            tmp = tot_maze[i][j][k].move(tot_maze, i, j, k)
                        elif tot_maze[i][j][k] == 2:
                            isthere[2] = 1
                        elif tot_maze[i][j][k] == 3:
                            isthere[3] = 1
                        if tmp == 0:
                            k += 1
                    
                    if isthere[0] and isthere[1]:
                        flag = self.pacman.crash()
                        if flag:
                            for k in range(len(tot_maze[i][j])):
                                if type(tot_maze[i][j][k]) in self.ghosts:
                                    del tot_maze[i][j][k]
                                    break

                    to_delete = []
                    if isthere[0] and isthere[2]:
                        to_delete.append(2)
                        self.pacman.eat_dot(self.dots)
                    if isthere[0] and isthere[3]:
                        to_delete.append(3)
                        self.pacman.eat_dot(self.power_dots)
                    
                    k = 0
                    while (k < len(tot_maze[i][j])):
                        if tot_maze[i][j][k] == 2 and 2 in to_delete:
                            tot_maze[i][j][k] = 0
                            break
                        if tot_maze[i][j][k] == 3 and 3 in to_delete:
                            tot_maze[i][j][k] = 0
                            break
                        k += 1
            
    def move_maze(self):
        if self.pacman.x > SCREEN_WIDTH/2:
            self.xgap -= self.pacman.x - SCREEN_WIDTH/2
            self.pacman.x = SCREEN_WIDTH/2
        if self.pacman.y > SCREEN_HEIGHT/2:
            self.ygap -= self.pacman.y - SCREEN_HEIGHT/2
            self.pacman.y = SCREEN_HEIGHT/2
        if self.xgap <= -30:
            self.xgap = -10
            self.maze.shift_map_x()
        if self.ygap <= -30:
            self.ygap = -10
            self.maze.shift_map_y()
    
    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)
        
        # TODO: 모든 게임 객체 그리기
        self.maze.draw(self.screen, self.ygap, self.xgap)
        
        tot_maze = self.maze.tot_maze
        for i in range(MAX_Y + 1):
            for j in range(MAX_X + 1):
                for k in tot_maze[i][j]:
                    if type(k) != int:
                        k.draw(self.screen, i, j, self.ygap, self.xgap)
                    elif k == 2:
                        self.dots.draw(self.screen, i, j, self.ygap, self.xgap)
                    elif k == 3:
                        self.power_dots.draw(self.screen, i, j, self.ygap, self.xgap)
        
        # self.pacman.draw(self.screen, 20, 20, -10, -10)
        
        # for ghost in self.ghosts:
        #     ghost.draw(self.screen, 10, 10, -10, -10)
        
        # TODO: 점수, 생명 등 UI 그리기
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """UI 요소 그리기"""
        # TODO: 점수, 생명, 게임 오버 메시지 등 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
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
            self.move_maze()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """프로그램 진입점"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()