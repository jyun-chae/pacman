import pygame
import sys

from Constants import *

pygame.init()

# 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Map_builder")

# 폰트
font = pygame.font.SysFont(None, 40)

# 버튼 클래스
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    def draw(self, surface):    # 출력
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 3)
        txt = font.render(self.text, True, WHITE)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def handle_event(self, event):  # 눌렸는가?
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# 초기 변수
row = 1
col = 1
state = "menu"  # 현재 상태

# row/col 증가/감소 함수
def increase_row():
    global row
    row += 1

def decrease_row():
    global row
    if row > 1:
        row -= 1

def increase_col():
    global col
    col += 1

def decrease_col():
    global col
    if col > 1:
        col -= 1

def start_game():
    global state
    state = "grid"

# 버튼 생성
buttons = [
    Button((SCREEN_WIDTH*7/36, SCREEN_HEIGHT/4, SCREEN_WIDTH/9, SCREEN_WIDTH/18), "up", increase_row),
    Button((SCREEN_WIDTH*7/36, SCREEN_HEIGHT*19/40, SCREEN_WIDTH/9, SCREEN_WIDTH/18), "down", decrease_row),
    Button((SCREEN_WIDTH*25/36, SCREEN_HEIGHT/4, SCREEN_WIDTH/9, SCREEN_WIDTH/18), "up", increase_col),
    Button((SCREEN_WIDTH*25/36, SCREEN_HEIGHT*19/40, SCREEN_WIDTH/9, SCREEN_WIDTH/18), "down", decrease_col),
    Button((SCREEN_WIDTH*7/16, SCREEN_HEIGHT*4/5, SCREEN_WIDTH/8, SCREEN_HEIGHT/12), "Start", start_game)
]

types = [BLACK, WHITE, DARK_GRAY, YELLOW, RED, PINK, CYAN, ORANGE]  # maze 안에 들어가는 색 종류들
flag = True

# 메인 루프
while True:
    screen.fill(BLACK)
    end = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            end = True
            break
        if state == "menu":
            for btn in buttons:
                btn.handle_event(event)
        if state == "grid":
            if flag:
                cell_width = SCREEN_WIDTH / col
                cell_height = SCREEN_HEIGHT / row
                li = list(list(0 for i in range(col)) for j in range(row))  # 여기서 생성하는 map 저장
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:    # 누른 경우 li값 변경 -> 수정
                xp, yp = event.pos
                iy = int(yp/cell_height)
                ix = int(xp/cell_width)
                li[iy][ix] += 1
                if li[iy][ix] >= 8:
                    li[iy][ix] = 0


    if end:
        break
    
    if state == "menu":
        # 텍스트
        row_text = font.render("Row", True, WHITE)
        row_rect = row_text.get_rect(center = (SCREEN_WIDTH/4, SCREEN_HEIGHT/6))
        col_text = font.render("Col", True, WHITE)
        col_rect = col_text.get_rect(center = (SCREEN_WIDTH*3/4, SCREEN_HEIGHT/6))
        screen.blit(row_text, row_rect)
        screen.blit(col_text, col_rect)

        row_val = font.render(str(row), True, WHITE)
        row_val_rect = row_val.get_rect(center = (SCREEN_WIDTH/4, SCREEN_HEIGHT*2/5))
        col_val = font.render(str(col), True, WHITE)
        col_val_rect = col_val.get_rect(center = (SCREEN_WIDTH*3/4, SCREEN_HEIGHT*2/5))
        screen.blit(row_val, row_val_rect)
        screen.blit(col_val, col_val_rect)

        # 버튼들
        for btn in buttons:
            btn.draw(screen)

    elif state == "grid":
        screen.fill(BLACK)
        for i in range(row):
            for j in range(col):    # 흰색 태두리 그리는중
                x = j * cell_width
                y = i * cell_height
                rect = pygame.Rect(x, y, cell_width, cell_height)
                pygame.draw.rect(screen, types[li[i][j]], rect, 0)
                
                pygame.draw.line(screen, WHITE, (x, y), (x + cell_width, y), 2)               # 윗변
                pygame.draw.line(screen, WHITE, (x + cell_width, y), (x + cell_width, y + cell_height), 2)  # 오른쪽
                pygame.draw.line(screen, WHITE, (x + cell_width, y + cell_height), (x, y + cell_height), 2) # 아랫변
                pygame.draw.line(screen, WHITE, (x, y + cell_height), (x, y), 2)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# 끝나면 파일에 저장
with open('./datas/map.txt', 'w', encoding='utf-8') as file:
    file.write(f"{row} {col}\n")
    for i in range(row):
        for j in range(col):
            file.write(f"{li[i][j] + 1} ")  # default값이 0이었기에 1 더해서 저장
        file.write("\n")