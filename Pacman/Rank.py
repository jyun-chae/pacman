import pygame

from Constants import *

class Ranking():
    def __init__(self, screen):
        self.rank = []
        self.draw_intro(screen)

    def read_txt(self, filename = "./datas/ranking.txt"):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            li = []
            for i in range(len(lines)):
                if lines[i] == '\n':
                    continue
                li.append(int(lines[i]))
            
            li.sort(reverse = True)
            
            if len(li) > 5:
                self.rank = li[:5]
                return li[:5]
            self.rank = li
            return li
        except Exception:
            raise Exception("ranking.txt 파일에 문제가 생겼습니다.")

    def draw_intro(self, screen):
        large_font = pygame.font.SysFont(None, 80)   # 큰 글씨
        medium_font = pygame.font.SysFont(None, 40)  # 중간 글씨
        small_font = pygame.font.SysFont(None, 30)   # 작은 글씨
        
        screen.fill(BLACK)
        title_surface = large_font.render("P.M.", True, YELLOW)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surface, title_rect)
        
        for idx, score in enumerate(self.rank):
            score_surface = small_font.render(f"{idx+1}. {score}", True, WHITE)
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 200 + idx * 40))
            screen.blit(score_surface, score_rect)

        time_attack_text = medium_font.render("Time_Attack", True, WHITE)
        self.time_attack_rect = time_attack_text.get_rect()
        self.time_attack_box = pygame.Rect(30, SCREEN_HEIGHT - 60, self.time_attack_rect.width + 20, self.time_attack_rect.height + 10)
        pygame.draw.rect(screen, WHITE, self.time_attack_box, 2)  # 테두리만
        screen.blit(time_attack_text, (self.time_attack_box.x + 10, self.time_attack_box.y + 5))

        # 우측 하단 버튼: Infinite
        infinite_text = medium_font.render("Infinite", True, WHITE)
        self.infinite_rect = infinite_text.get_rect()
        self.infinite_box = pygame.Rect(SCREEN_WIDTH - self.infinite_rect.width - 50, SCREEN_HEIGHT - 60,
                                self.infinite_rect.width + 20, self.infinite_rect.height + 10)
        pygame.draw.rect(screen, WHITE, self.infinite_box, 2)
        screen.blit(infinite_text, (self.infinite_box.x + 10, self.infinite_box.y + 5))
        
        pygame.display.flip()
    
    def is_box_clicked(box_rect, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 왼쪽 클릭
            if box_rect.collidepoint(event.pos):
                return True
        return False
    
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            if Ranking.is_box_clicked(self.time_attack_box, event):
                return 2

            if Ranking.is_box_clicked(self.infinite_box, event):
                return 3
        return 1
    
    def insert_score(self, score, file_name = "./datas/ranking.txt"):
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"\n{score}")  # 줄 바꾸고 숫자 추가