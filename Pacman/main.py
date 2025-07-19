'''
일부 아이디어는 스팀에 팩맨 관련 게임에서 모티브 받았음을 알립니다
필요없는 method들을 삭제했습니다
필요한 로직들은 전부 구현했습니다
충돌 감지는 x, y값 비교로 진행했습니다
점수 나옵니다
게임 오버는 되지만 승리는 없습니다. 시간제한은 존재합니다
맵이 계속해서 움직입니다(모티브 받음) -> 이것만으로 모든걸 뜯어 고치고 겁나 힘들었습니다 (사실 map을 사람이 제작 가능하게 할 생각만 없었어도 쉬웠을거 같은데 초기 아이디어가 그거라..)
맵을 사람이 제작 가능합니다 -> 여러가지 컨셉적인 맵이 가능합니다
각 ghost별로 특수한 특징들이 존재합니다. 기존의 팩맨은 로직이 많이 단순합니다. ghost.py에서 추가적으로 설명합니다
ghost에게 계속해서 쫒기는 상황에서 한쪽 방향으로만 맵이 확장되기에 지속적인 모험을 강제합니다
시간제한이 있는 버전과 없는 버전이 존재합니다
기본적으로 맵을 계속해서 확장할수 밖에 없도록 맵을 제작하기 때문에 확장할수록 반복되는 맵에 변화를 주어야 하는데 이를 ghost들의 생성 확률을 도입하여 해결하였습니다
power pellet도 확률 도입 충분히 가능합니다. 돈만 주시면 해드립니다
랭킹 시스템 구현했습니다
어떠한 상황, 어떠한 화면 크기, fps, cell_size 모두 사용 가능하도록 const를 적극적으로 사용하여서 제작했습니다
사용자가 쉽게 손댈 수 있는 txt 파일을 읽는 과정에는 따로 exception message를 넣었습니다
모티브 받음 게임과의 차이점은 ghost적인 부분과 맵을 커스텀 가능하다는 점과 x,y축 모두 움직인다, 외부적인 요인을 제외하고도 ghost만으로도 맵의 이동을 강제한다는 점 등 많습니다
'''
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
from Rank import *

class Game:
    """게임 메인 클래스"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("팩맨 게임")
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.game_over = False
        self.game_won = False
        
        # 모드 종류 구분
        self.time_limit = -1
        # 터지고 있는 폭단 리스트
        self.bombs = []
        
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
        
        # 화면이 움직인 정도
        self.ygap = -10
        self.xgap = -10
        
        # 시간 흐름 정도
        self.level = 0
    
    # 다음판 시작시 초기화 함수
    def reset(self, time_limit):
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.game_over = 0
        self.game_won = False
        
        self.time_limit = time_limit
        
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
        
        self.level = 0
    
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
            
            # 시간초과 확인
            if self.time_limit != -1 and 10*self.level >= self.time_limit:
                self.game_over = 1
                return
            
            #현재 maze상태 다운로드
            tot_maze = self.maze.tot_maze
            
            ghosts = []
            is_pacman = 1
            for i in range(MAX_Y + 1):
                for j in range(MAX_X + 1):
                    isthere = [0,0,0,0] # 팩맨, 유령, 점, 파워점 해당 칸에 존재하는지 확인
                    if len(tot_maze[i][j]) == 1 and type(tot_maze[i][j][0]) == int: # object 없으면 굳이 실행X
                        continue
                    k = 0
                    while (k < len(tot_maze[i][j])):
                        tmp = 0
                        if type(tot_maze[i][j][k]) == Pacman:   # 팩맨 찾으면 팩맨 이동
                            is_pacman = 0
                            self.pacman = tot_maze[i][j][k]
                            isthere[0] = 1
                            tmp = tot_maze[i][j][k].move(tot_maze, i ,j, k, self.pacman)
                        elif type(tot_maze[i][j][k]) in self.ghosts:    # ghost 이동 + bomb는 터져야 하면 터뜨림
                            isthere[1] = 1
                            tmp, gst = tot_maze[i][j][k].move(tot_maze, i, j, k, self.pacman)
                            if tmp == -1:
                                self.bombs.append([i, j, pygame.time.get_ticks()])
                                tot_maze[i][j].pop(k)
                                tmp = 1
                            ghosts.append([gst,gst.i,gst.j])
                        elif tot_maze[i][j][k] == 2:
                            isthere[2] = 1
                        elif tot_maze[i][j][k] == 3:
                            isthere[3] = 1
                        if tmp == 0:    # move에서 반환된 값을 기반으로 움직였는지 판단 -> 움직였으면 k증가 X
                            k += 1

                    to_delete = []
                    if isthere[0] and isthere[2]:   # 점을 팩맨이 먹은경우
                        to_delete.append(2)
                        self.pacman.eat_dot(self.dots)
                    if isthere[0] and isthere[3]:   # 파워점을 팩맨이 먹은경우
                        to_delete.append(3)
                        self.pacman.eat_dot(self.power_dots)
                    
                    k = 0
                    while (k < len(tot_maze[i][j])):    # 먹으면 지워야지
                        if tot_maze[i][j][k] == 2 and 2 in to_delete:
                            tot_maze[i][j][k] = 0
                            break
                        if tot_maze[i][j][k] == 3 and 3 in to_delete:
                            tot_maze[i][j][k] = 0
                            break
                        k += 1
            
            # 낮은 확률로 충돌 무시하는걸 방지하기 위해서 index값 비교가 아닌 출력 좌표로 충돌 비교
            for i in range(len(ghosts)):
                if (abs(ghosts[i][0].x - self.pacman.x) < 5) and (abs(ghosts[i][0].y - self.pacman.y) < 5):
                    flag = self.pacman.crash()
                    if flag:
                        for k in range(len(tot_maze[ghosts[i][1]][ghosts[i][2]])):
                                if type(tot_maze[ghosts[i][1]][ghosts[i][2]][k]) in self.ghosts:
                                    del tot_maze[ghosts[i][1]][ghosts[i][2]][k]
                                    break
            
            # power up 상태 관리
            if self.pacman.is_powered_up:
                self.pacman.power_up_timer += 1
            if self.pacman.is_powered_up and self.pacman.power_up_timer >= self.pacman.power_up_max:
                self.pacman.power_up_timer = 0
                self.pacman.is_powered_up = False
            # 몇픽셀 이상 등장 안한경우 게임 끝냄 -> 낮은 확률로 가끔 터질때도 있어서 5픽셀로 제한
            if is_pacman:
                is_pacman += 1
                if (is_pacman > 5):
                    self.game_over = 1
            # 피가 다 단 경우 게임 끝냄
            if self.pacman.lives <= 0:
                self.game_over = 1
            
            
    def move_maze(self):
        if not self.game_over and not self.game_won:
            # 시간 측정
            self.level = (pygame.time.get_ticks() - self.start_time)/10000
            # 팩맨의 위치가 중간에서 넘어간다면 그만큼 maze 이동
            if self.pacman.x > SCREEN_WIDTH/2:
                self.xgap -= self.pacman.x - SCREEN_WIDTH/2
                self.pacman.x = SCREEN_WIDTH/2
            if self.pacman.y > SCREEN_HEIGHT/2:
                self.ygap -= self.pacman.y - SCREEN_HEIGHT/2
                self.pacman.y = SCREEN_HEIGHT/2
            # 한칸이 넘어갈 경우 shift 실행
            if self.xgap <= -30:
                self.xgap = -10
                self.maze.shift_map_x(int(self.level))
            if self.ygap <= -30:
                self.ygap = -10
                self.maze.shift_map_y(int(self.level))
    
    def draw(self):
        """화면 그리기"""
        self.screen.fill(BLACK)
        
        # TODO: 모든 게임 객체 그리기
        self.maze.draw(self.screen, self.ygap, self.xgap)
    
        tot_maze = self.maze.tot_maze
        for i in range(MAX_Y + 1):
            for j in range(MAX_X + 1):
                for k in tot_maze[i][j]:
                    # object면 draw를 전부 가지고 있기에 int가 아니면 그냥 실행
                    if type(k) != int:
                        k.draw(self.screen, i, j, self.ygap, self.xgap)
                    elif k == 2:
                        self.dots.draw(self.screen, i, j, self.ygap, self.xgap)
                    elif k == 3:
                        self.power_dots.draw(self.screen, i, j, self.ygap, self.xgap)
        
        # 폭탄이 터진경우 짧은 시간동안 터뜨림
        idx = 0
        while (idx < len(self.bombs)):
            if (pygame.time.get_ticks() - self.bombs[idx][2])/100 > 1:
                self.bombs.pop(idx)
            else:
                self.bob(self.bombs[idx][0], self.bombs[idx][1])
            idx += 1
        
        # TODO: 점수, 생명 등 UI 그리기
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """UI 요소 그리기"""
        # TODO: 점수, 생명, 게임 오버 메시지 등 표시
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.pacman.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        life_text = font.render(f"Life: {self.pacman.lives}", True, WHITE)
        self.screen.blit(life_text, (10, 40))
        life_text = font.render(f"Time: {10*self.level:.2f}", True, WHITE)
        self.screen.blit(life_text, (10, 70))
        
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            self.game_over += 1
    
    def run(self):
        """게임 메인 루프"""
        while self.running:
            # game_over후 5초가 지나면 매인화면 복귀
            if (self.game_over > FPS*5):
                return 1
            self.handle_events()
            self.update()
            self.draw()
            self.move_maze()
            self.clock.tick(FPS)
        # self.running즉 그냥 pygame 창을 꺼버린 경우
        return -1

    # 폭발 출력
    def bob(self, i, j):
        rect = pygame.Rect(j*CELL_SIZE - CELL_SIZE*5, i*CELL_SIZE - CELL_SIZE*5, CELL_SIZE*11, CELL_SIZE*11)
        pygame.draw.rect(self.screen, RED, rect)
        if abs(self.pacman.iy - i) <= 5 and abs(self.pacman.ix - j) <= 5:
            self.pacman.crash()

def main():
    """프로그램 진입점"""
    game = Game()
    rank = Ranking(game.screen) # 랭킹 관련 객체
    flag = 1    # 현재 화면 단계
    while True:
        if flag == 1:   # 매인화면
            rank.read_txt()
            while flag == 1:
                rank.draw_intro(game.screen)
                flag = rank.update()
            
        if flag == 2:   # time attack 상태
            game.reset(60)  # 60초 제한
            flag = game.run()
            rank.insert_score(game.pacman.score)    # 점수 추가
        
        if flag == 3:   # 무한모드
            game.reset(-1)  # 제한 없음
            flag = game.run()
            rank.insert_score(game.pacman.score)
        
        if flag == -1:  # 게임창 강제종료
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
    
"""
구현 과제 체크리스트:
===================

필수 구현 사항:
□ MovableObject의 move() 메서드 구현    -> 완료
□ MovableObject의 can_move() 메서드 구현    -> update에서 방향 설정하면서 벽까지 확인하는 형태로 함축시켰습니다
□ Pacman의 update() 메서드 완성 -> 완료
□ Pacman의 eat_dot() 메서드 구현    -> 그냥 점수만 올리는 것을 중점으로 구현
□ Ghost의 chase_pacman() 메서드 구현    -> update에서 방향 설정하는 과정 안에 포함되도록 함축시켰습니다
□ Ghost의 flee_from_pacman() 메서드 구현    -> 완료
□ 각 유령(Blinky, Pinky, Inky, Clyde)의 고유한 AI 패턴 구현 -> 완료
□ Maze의 is_wall() 메서드 구현  -> 굳이 필요 없어서 삭제했습니다 각자 update하는 과정에서 벽의 여부 확인합니다
□ Game의 check_collisions() 메서드 구현 -> 처음에는 구현 생각이 없었는데 어쩌다 보니 비슷한게 생기긴 했습니다(유령 충돌을 x, y값을 기반으로 진행 하지만 번거로울 수 있어서 함수로는 안뺌)
□ Game의 check_win_condition() 메서드 구현  -> 이런게 있었네 아무튼 내용은 안에 들어가 있습니다. 시간초과, hp등 확인해서 끝내는거 포함됨

코드 작성 팁:
- 객체 간의 상호작용을 명확히 정의하세요
- 각 클래스의 책임을 명확히 구분하세요
- 상속을 적절히 활용하여 코드 중복을 줄이세요
- 주석을 충분히 작성하여 코드의 가독성을 높이세요
- Git을 사용하여 버전 관리를 하면 가산점이 있습니다

행운을 빕니다!
"""