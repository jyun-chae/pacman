import pygame

from Constants import *

class Ranking():    # 랭킹 읽기 및 초기화면 출력
    def __init__(self, screen):
        self.rank = []
        self.draw_intro(screen)

    def read_txt(self, filename = "./datas/ranking.txt"):   # 랭킹 읽는중
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            li = []
            for i in range(len(lines)):
                if lines[i] == '\n':
                    continue
                li.append(int(lines[i]))
            
            li.sort(reverse = True)
            
            if len(li) > 5: # 상위 5명만 기억
                self.rank = li[:5]
                return li[:5]
            self.rank = li
            return li
        except Exception:
            raise Exception("ranking.txt 파일에 문제가 생겼습니다.")    # 뭔가 이상함

    def draw_intro(self, screen):
        large_font = pygame.font.SysFont(None, 80)   # 큰 글씨
        medium_font = pygame.font.SysFont(None, 40)  # 중간 글씨
        small_font = pygame.font.SysFont(None, 30)   # 작은 글씨
        # pacman줄임말 p.m. 있어보이지 않음?
        screen.fill(BLACK)
        title_surface = large_font.render("P.M.", True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surface, title_rect)
        
        for idx, score in enumerate(self.rank): # 상위사람들 출력 하지만 없으면 안함
            score_surface = small_font.render(f"{idx+1}. {score}", True, WHITE)
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 200 + idx * 40))
            screen.blit(score_surface, score_rect)

        time_attack_text = medium_font.render("Time_Attack", True, WHITE)   # time attack 모드 버튼
        self.time_attack_rect = time_attack_text.get_rect()
        self.time_attack_box = pygame.Rect(30, SCREEN_HEIGHT - 60, self.time_attack_rect.width + 20, self.time_attack_rect.height + 10)
        pygame.draw.rect(screen, WHITE, self.time_attack_box, 2)  # 테두리만
        screen.blit(time_attack_text, (self.time_attack_box.x + 10, self.time_attack_box.y + 5))

        infinite_text = medium_font.render("Infinite", True, WHITE) # infinite 모드 버튼
        self.infinite_rect = infinite_text.get_rect()
        self.infinite_box = pygame.Rect(SCREEN_WIDTH - self.infinite_rect.width - 50, SCREEN_HEIGHT - 60,
                                self.infinite_rect.width + 20, self.infinite_rect.height + 10)
        pygame.draw.rect(screen, WHITE, self.infinite_box, 2)
        screen.blit(infinite_text, (self.infinite_box.x + 10, self.infinite_box.y + 5))
        
        pygame.display.flip()
    
    def is_box_clicked(box_rect, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 좌클릭
            if box_rect.collidepoint(event.pos):
                return True
        return False
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # 겜 꺼짐
                return -1

            if Ranking.is_box_clicked(self.time_attack_box, event): # 시간제한 모드
                return 2

            if Ranking.is_box_clicked(self.infinite_box, event):    # 한무모드
                return 3
        return 1
    
    def insert_score(self, score, file_name = "./datas/ranking.txt"):   # 점수 추가
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"\n{score}")  # 줄 바꾸고 숫자 추가