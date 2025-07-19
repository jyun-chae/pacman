from enum import Enum

# 모든 상수값 저장해두는 장소 내 입맞데로 몇개 수정함

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120
CELL_SIZE = 20

MAX_X = SCREEN_WIDTH//CELL_SIZE
MAX_Y = SCREEN_HEIGHT//CELL_SIZE

LEVELS = [2, 4, 6, 8, 10]

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

class Direction(Enum):
    """방향을 나타내는 열거형 클래스"""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    NONE = (0, 0)