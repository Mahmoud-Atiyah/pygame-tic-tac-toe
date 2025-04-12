import pygame
import sys
import random
import copy

# --- Game Config ---
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 4
FONT_SIZE = 50

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# Difficulty: 'easy', 'medium', 'hard'
def get_difficulty():
    while True:
        print("Select Difficulty: [easy] [medium] [hard]")
        diff = input("Enter difficulty: ").strip().lower()
        if diff in ['easy', 'medium', 'hard']:
            return diff
        else:
            print("Invalid input. Please choose 'easy', 'medium', or 'hard'.")

DIFFICULTY = get_difficulty()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe - Pygame Edition")
font = pygame.font.SysFont(None, FONT_SIZE)
board = [[3 * i + j + 1 for j in range(3)] for i in range(3)]
game_over = False

def draw_board():
    screen.fill(BG_COLOR)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            mark = board[i][j]
            if mark == 'X':
                draw_x(i, j)
            elif mark == 'O':
                draw_o(i, j)

def draw_x(row, col):
    offset = SQUARE_SIZE // 4
    start = (col * SQUARE_SIZE + offset, row * SQUARE_SIZE + offset)
    end = (col * SQUARE_SIZE + SQUARE_SIZE - offset, row * SQUARE_SIZE + SQUARE_SIZE - offset)
    pygame.draw.line(screen, X_COLOR, start, end, LINE_WIDTH)
    pygame.draw.line(screen, X_COLOR, (start[0], end[1]), (end[0], start[1]), LINE_WIDTH)

def draw_o(row, col):
    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.circle(screen, O_COLOR, center, CIRCLE_RADIUS, LINE_WIDTH)

def get_square(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2]:
            return b[i][0]
        if b[0][i] == b[1][i] == b[2][i]:
            return b[0][i]
    if b[0][0] == b[1][1] == b[2][2]:
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0]:
        return b[0][2]
    return None

def is_draw(b):
    return all(cell in ('X', 'O') for row in b for cell in row)

def minimax(b, is_max):
    winner = check_winner(b)
    if winner == 'O': return 1
    if winner == 'X': return -1
    if is_draw(b): return 0

    if is_max:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] not in ('X', 'O'):
                    b[i][j] = 'O'
                    score = minimax(b, False)
                    b[i][j] = 3 * i + j + 1
                    best = max(best, score)
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if b[i][j] not in ('X', 'O'):
                    b[i][j] = 'X'
                    score = minimax(b, True)
                    b[i][j] = 3 * i + j + 1
                    best = min(score, best)
        return best

def best_move(b):
    if DIFFICULTY == 'easy':
        available = [(i, j) for i in range(3) for j in range(3) if b[i][j] not in ('X', 'O')]
        return random.choice(available) if available else None

    if DIFFICULTY == 'medium' and random.random() < 0.5:
        return best_move(copy.deepcopy(b))  # recursive fallback to 'easy'

    best = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if b[i][j] not in ('X', 'O'):
                b[i][j] = 'O'
                score = minimax(b, False)
                b[i][j] = 3 * i + j + 1
                if score > best:
                    best = score
                    move = (i, j)
    return move

def show_result(winner):
    global game_over
    game_over = True
    text = "Draw!" if winner is None else f"{winner} wins!"
    msg = font.render(text, True, (255, 255, 255))
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)
    restart()

def restart():
    global board, game_over
    board = [[3 * i + j + 1 for j in range(3)] for i in range(3)]
    game_over = False

def show_menu():
    global DIFFICULTY
    screen.fill(BG_COLOR)
    title = font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))

    difficulties = ['easy', 'medium', 'hard']
    buttons = []

    for i, level in enumerate(difficulties):
        rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + i * 70, 200, 50)
        pygame.draw.rect(screen, LINE_COLOR, rect)
        text = font.render(level.capitalize(), True, (0, 0, 0))
        screen.blit(text, (rect.x + 50, rect.y + 10))
        buttons.append((rect, level))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, level in buttons:
                    if rect.collidepoint(event.pos):
                        DIFFICULTY = level
                        return

# --- Main Loop ---
show_menu()
draw_board()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square(event.pos)
            if board[row][col] not in ('X', 'O'):
                board[row][col] = 'X'
                draw_board()
                pygame.display.update()

                if check_winner(board) or is_draw(board):
                    show_result(check_winner(board))
                    continue

                ai_move = best_move(copy.deepcopy(board))
                if ai_move:
                    board[ai_move[0]][ai_move[1]] = 'O'
                    draw_board()
                    pygame.display.update()

                if check_winner(board) or is_draw(board):
                    show_result(check_winner(board))

    if not game_over:
        draw_board()
        pygame.display.update()