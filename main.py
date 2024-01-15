from typing import Any
import pygame
import os
import sys
import random

pygame.init()
size = width, height = 800, 700
screen = pygame.display.set_mode(size)

COLORS = {
    "blue": "Tetris in pygame/images/blue.png",
    "green": "Tetris in pygame/images/green.png",
    "lightblue": "Tetris in pygame/images/lightblue.png",
    "pink": "Tetris in pygame/images/pink.png",
    "red": "Tetris in pygame/images/red.png",
    "verylightblue": "Tetris in pygame/images/verylightblue.png",
    "yellow": "Tetris in pygame/images/yellow.png",
}

SHAPES = {
    1: [[[1, 1], [1, 1]]],
    2: [
        [[1, 1, 1], [1, 0, 0]],
        [[1, 0], [1, 0], [1, 1]],
        [[0, 0, 1], [1, 1, 1]],
        [[1, 1], [0, 1], [0, 1]],
    ],
    3: [[[1, 1, 1, 1]], [[1], [1], [1], [1]]],
    4: [[[1, 1, 0], [0, 1, 1]], [[0, 1], [1, 1], [1, 0]]],
    5: [
        [[1, 1, 1], [0, 0, 1]],
        [[0, 1], [0, 1], [1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
    ],
    6: [[[0, 1, 1], [1, 1, 0]], [[1, 0], [1, 1], [0, 1]]],
    7: [
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]],
    ],
}


def load_image(name, colorkey=None):
    name
    # если файл не существует, то выходим
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


LETTERS = {
    "A": "Tetris in pygame/images/letters/A.jpg",
    "B": "Tetris in pygame/images/letters/B.jpg",
    "C": "Tetris in pygame/images/letters/C.jpg",
    "D": "Tetris in pygame/images/letters/D.jpg",
    "E": "Tetris in pygame/images/letters/E.jpg",
    "F": "Tetris in pygame/images/letters/F.jpg",
    "G": "Tetris in pygame/images/letters/G.jpg",
    "H": "Tetris in pygame/images/letters/H.jpg",
    "I": "Tetris in pygame/images/letters/I.jpg",
    "J": "Tetris in pygame/images/letters/J.jpg",
    "K": "Tetris in pygame/images/letters/K.jpg",
    "L": "Tetris in pygame/images/letters/L.jpg",
    "M": "Tetris in pygame/images/letters/M.jpg",
    "N": "Tetris in pygame/images/letters/N.jpg",
    "O": "Tetris in pygame/images/letters/O.jpg",
    "P": "Tetris in pygame/images/letters/P.jpg",
    "Q": "Tetris in pygame/images/letters/Q.jpg",
    "R": "Tetris in pygame/images/letters/R.jpg",
    "S": "Tetris in pygame/images/letters/S.jpg",
    "T": "Tetris in pygame/images/letters/T.jpg",
    "U": "Tetris in pygame/images/letters/U.jpg",
    "V": "Tetris in pygame/images/letters/V.jpg",
    "W": "Tetris in pygame/images/letters/W.jpg",
    "X": "Tetris in pygame/images/letters/X.jpg",
    "Y": "Tetris in pygame/images/letters/Y.jpg",
    "Z": "Tetris in pygame/images/letters/Z.jpg",
    "+": "Tetris in pygame/images/letters/+.jpg",
    "0": "Tetris in pygame/images/letters/0.jpg",
    "1": "Tetris in pygame/images/letters/1.jpg",
    "2": "Tetris in pygame/images/letters/2.jpg",
    "3": "Tetris in pygame/images/letters/3.jpg",
    "4": "Tetris in pygame/images/letters/4.jpg",
    "5": "Tetris in pygame/images/letters/5.jpg",
    "6": "Tetris in pygame/images/letters/6.jpg",
    "7": "Tetris in pygame/images/letters/7.jpg",
    "8": "Tetris in pygame/images/letters/8.jpg",
    "9": "Tetris in pygame/images/letters/9.jpg",
    ":": "Tetris in pygame/images/letters/double point.jpg",
}

font_key = load_image(LETTERS["A"]).get_at((0, 0))


def convert_text(screen, pos: list, text: str):
    x = pos[0]
    y = pos[1]
    for i in text:
        if i.upper() in LETTERS:
            image = load_image(LETTERS[i.upper()], font_key)
            if image.get_height() < 28:
                y = pos[1] + (28 - image.get_height()) / 2
            screen.blit(image, [x, y])
            x += image.get_width() + 2
            y = pos[1]
        elif i == " ":
            x += 20


def clear_line(board):
    global score_game
    for i in enumerate(board.board):
        for j in i[1]:
            if j != 1:
                break
        else:
            kills = []
            for j in dots:
                if j.pos[1] == i[0]:
                    kills.append(j)
                    j.kill()
            for j in kills:
                dots.remove(j)
            for j in range(len(board.board[i[0]])):
                board.board[i[0]][j] = 0
            flag = True
            while flag:
                flag = False
                for j in dots:
                    if j.pos[1] < i[0]:
                        if j.update_pos([j.pos[0], j.pos[1] + 1]):
                            flag = True
            for j in range(len(board.board)):
                for k in range(len(board.board[0])):
                    board.board[j][k] = 0
            for j in dots:
                j.update_pos(j.pos)
            score_game = score(screen, "clear", score_game)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 24

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        pygame.draw.rect(
            screen,
            "white",
            (
                (self.left, self.top),
                (self.width * self.cell_size, self.height * self.cell_size),
            ),
            1,
        )


class Dot(pygame.sprite.Sprite):
    def __init__(self, color: str, coord: list, board: "Board"):
        if color not in COLORS:
            raise NameError
        self.image = load_image(COLORS[color])
        super().__init__(all_sprites)
        self.board = board
        self.rect = self.image.get_rect()
        self.pos = coord
        self.width = self.rect.width
        self.height = self.rect.height
        self.update_pos(self.pos)

    def update_pos(self, coord):
        try:
            if self.board.board[coord[1]][coord[0]] != 1 and coord[0] >= 0:
                self.board.board[self.pos[1]][self.pos[0]] = 0
                self.board.board[coord[1]][coord[0]] = 1
                self.rect.x = coord[0] * board.cell_size + board.left
                self.rect.y = coord[1] * board.cell_size + board.top
                self.pos = coord
            else:
                return False
            return True
        except IndexError:
            if coord[1] >= len(self.board.board):
                return "floor"
            return False


class Shape:
    def __init__(self, coord: list, shape_index, color, board: "Board"):
        self.shape = SHAPES[shape_index]
        self.color = color
        self.col = 0
        self.pos = coord
        self.board = board
        self.len = 0
        y = self.pos[1]
        for shape in enumerate(self.shape[self.col]):
            x = self.pos[0]
            for j in enumerate(shape[1]):
                if j[1]:
                    self.shape[self.col][shape[0]][j[0]] = Dot(
                        self.color, [x, y], board
                    )
                    dots.append(self.shape[self.col][shape[0]][j[0]])
                    self.len += 1
                x += 1
            y += 1

    def update(self):
        if self.pos[1] + len(self.shape[self.col]) < len(self.board.board):
            for i in range(len(self.shape[self.col][0])):
                for j in range(len(self.shape[self.col]) - 1, -1, -1):
                    if self.shape[self.col][j][i]:
                        if self.board.board[self.pos[1] + j + 1][self.pos[0] + i] == 1:
                            return True
                        break
            else:
                self.pos[1] += 1
                if self.update_pos_right_down(self.pos):
                    return True
        else:
            return True

    def update_pos_right_down(self, pos):
        try:
            flag = True
            y = pos[1]
            for shape in enumerate(self.shape[self.col]):
                x = pos[0]
                for j in enumerate(shape[1]):
                    if (
                        j[1]
                        and self.board.board[y][x] == 1
                        and not self.shape[self.col][shape[0]][j[0]]
                    ):
                        flag = False
                    x += 1
                y += 1
        except IndexError:
            flag = False
        if pos[1] < len(self.board.board) and pos[1] >= 0 and flag:
            y = pos[1] + len(self.shape[self.col]) - 1
            for shape in reversed(self.shape[self.col]):
                x = pos[0] + len(shape) - 1
                for i in reversed(shape):
                    if i:
                        a = i.update_pos([x, y])
                        if a == "floor":
                            return True
                        elif not a:
                            return
                    x -= 1
                y -= 1
            self.pos = pos

    def update_pos_left_up(self, pos):
        try:
            flag = True
            y = pos[1]
            for shape in enumerate(self.shape[self.col]):
                x = pos[0]
                for j in enumerate(shape[1]):
                    if (
                        j[1]
                        and self.board.board[y][x] == 1
                        and not self.shape[self.col][shape[0]][j[0]]
                        or x == -1
                        or self.board.board[y][x] == 1
                        and x == pos[0]
                    ):
                        flag = False
                    x += 1
                y += 1
        except IndexError:
            flag = False
        if pos[1] < len(self.board.board) and pos[1] >= 0 and flag:
            y = pos[1]
            for shape in self.shape[self.col]:
                x = pos[0]
                for i in shape:
                    if i:
                        a = i.update_pos([x, y])
                        if a == "floor":
                            return True
                        elif not a:
                            return
                    x += 1
                y += 1
            self.pos = pos

    def move(self, v):
        if v == 1:
            self.update_pos_right_down([self.pos[0] + 1, self.pos[1]])
        elif v == 0:
            self.update_pos_left_up([self.pos[0] - 1, self.pos[1]])

    def rotate(self, v):
        if v == "right":
            if self.col + 1 >= len(self.shape):
                self.col = 0
                last = len(self.shape) - 1
            else:
                self.col += 1
                last = self.col - 1
        elif v == "left":
            if self.col == 0:
                self.col = len(self.shape) - 1
                last = 0
            else:
                self.col -= 1
                last = self.col + 1
        try:
            flag = True
            y = self.pos[1]
            for shape in enumerate(self.shape[self.col]):
                x = self.pos[0]
                for j in enumerate(shape[1]):
                    if (
                        j[1]
                        and self.board.board[y][x] == 1
                        and not self.shape[last][shape[0]][j[0]]
                    ):
                        flag = False
                    x += 1
                y += 1
        except IndexError:
            flag = False
        if (
            len(self.shape[self.col]) + self.pos[1] - 1 < len(self.board.board)
            and len(self.shape[self.col][0]) + self.pos[0] - 1
            < len(self.board.board[0])
            and flag
        ):
            for _ in range(self.len):
                dots.pop()
            y = self.pos[1]
            for shape in self.shape[last]:
                x = self.pos[0]
                for j in shape:
                    if j:
                        j.kill()
                        self.board.board[y][x] = 0
                    x += 1
                y += 1
            self.len = 0
            y = self.pos[1]
            for shape in enumerate(self.shape[self.col]):
                x = self.pos[0]
                for j in enumerate(shape[1]):
                    if j[1]:
                        self.shape[self.col][shape[0]][j[0]] = Dot(
                            self.color, [x, y], self.board
                        )
                        dots.append(self.shape[self.col][shape[0]][j[0]])
                        self.len += 1
                    x += 1
                y += 1
        else:
            self.col = last


def next_shape(pos, shape_index, color, screen):
    pygame.draw.rect(
        screen, "white", (pos, (board.cell_size * 6, board.cell_size * 4)), width=1
    )
    shape = SHAPES[shape_index]
    y = int(pos[1] + (board.cell_size * 4 - len(shape[0]) * board.cell_size) / 2)
    for i in shape[0]:
        x = int(pos[0] + (board.cell_size * 6 - len(shape[0][0]) * board.cell_size) / 2)
        for j in i:
            if j:
                image = load_image(COLORS[color])
                screen.blit(image, [x, y])
            x += board.cell_size
        y += board.cell_size


def start_screen(screen):
    image = load_image(
        "Tetris in pygame/images/Tetris.png"
    )
    screen.blit(image, [(width - image.get_width()) / 2, 100])
    convert_text(screen, [(width - 20 * 5) / 2, 300], "start")
    convert_text(screen, [(width - 20 * 10) / 2, 400], "liderboard")


def score(screen, event: str, scores: int):
    res = scores
    if event == "clear":
        res += 100
    elif event == "speed":
        res += 1
    convert_text(screen, [20, board.top + 70], f"score: {res}")
    return res


def game_over(screen, scores: int):
    game_width = 400
    game_height = 400
    pygame.draw.rect(
        screen,
        "black",
        (
            ((width - game_width) / 2, (height - game_height) / 2),
            (game_width, game_height),
        ),
    )
    pygame.draw.rect(
        screen,
        "white",
        (
            ((width - game_width) / 2, (height - game_height) / 2),
            (game_width, game_height),
        ),
        width=5,
    )
    convert_text(
        screen,
        [(width - game_width) / 2 + 100, (height - game_height) / 2 + 50],
        "game over",
    )
    convert_text(
        screen,
        [
            (width - game_width) / 2
            + (((width - game_width) - len(f"score: {scores}") * 20) / 2),
            (height - game_height) / 2 + 150,
        ],
        f"score: {scores}",
    )
    convert_text(
        screen,
        [
            (width - game_width) / 2 + (((width - game_width) - len("retry") * 20) / 2),
            (height - game_height) / 2 + 230,
        ],
        "retry",
    )
    convert_text(
        screen,
        [
            (width - game_width) / 2
            + (((width - game_width) - len("main menu") * 20) / 2),
            (height - game_height) / 2 + 310,
        ],
        "main menu",
    )


if __name__ == "__main__":
    all_sprites = pygame.sprite.Group()
    dots = []
    board = Board(10, 20)
    board.set_view((width - board.width * board.cell_size) / 2, 150, 24)
    shape = Shape(
        [4, 0], random.randrange(1, 8), random.choice(list(COLORS.keys())), board
    )

    running = True
    pygame.mixer.music.load(
        "Tetris in pygame/data/sounds/02. A-Type Music (v1.0).mp3"
    )
    pygame.mixer.music.play(-1)
    next_color = random.choice(list(COLORS.keys()))
    shape_index = random.randrange(1, 8)
    pygame.time.set_timer(pygame.USEREVENT, 300)
    past = None
    score_game = 0
    flag = False
    count = 0
    speed = False
    over = False
    movel = False
    mover = False
    clock = pygame.time.Clock()
    last = 0
    time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT and flag and not over:
                if shape.update():
                    clear_line(board)
                    if 1 not in board.board[1]:
                        shape = Shape([4, 0], shape_index, next_color, board)
                        shape_index = random.randrange(1, 8)
                        next_color = random.choice(list(COLORS.keys()))
                        count = 0
                    else:
                        count += 1
                        if count >= 5:
                            over = True
                if speed:
                    score_game = score(screen, "speed", score_game)
            if event.type == pygame.KEYDOWN and flag and not over:
                if event.key == 1073741904:
                    movel = True
                elif event.key == 1073741903:
                    mover = True
                elif event.key == 1073741906:
                    shape.rotate("right")
                elif event.key == 1073741905:
                    pygame.time.set_timer(pygame.USEREVENT, 100)
                    speed = True
            if event.type == pygame.KEYUP and flag and not over:
                if event.key == 1073741905:
                    pygame.time.set_timer(pygame.USEREVENT, 300)
                    speed = False
                elif event.key == 1073741904 or event.key == 1073741903:
                    movel = False
                    mover = False
            if event.type == pygame.MOUSEBUTTONDOWN and (not flag or over):
                if over:
                    pass
                if (width - 20 * 5) / 2 < event.pos[0] < 20 * 5 + (
                    width - 20 * 5
                ) / 2 and 300 < event.pos[1] < 300 + 28:
                    flag = True
                    pygame.mixer.music.load(
                        "Tetris in pygame/data/sounds/03. A-Type Music (Korobeiniki).mp3"
                    )
                    pygame.mixer.music.play(-1)
        if flag:
            screen.fill("black")
            next_shape(
                [board.left + board.width * board.cell_size + 50, board.top + 50],
                shape_index,
                next_color,
                screen,
            )
            time += clock.tick()
            if (time - last) // 100:
                last = time
                if movel:
                    shape.move(0)
                elif mover:
                    shape.move(1)
            all_sprites.draw(screen)
            board.render(screen)
            score(screen, "", score_game)
            tetris = load_image(
                "Tetris in pygame/images/Tetris.png"
            )
            screen.blit(tetris, ((width - tetris.get_width()) / 2, 10))
            if over:
                game_over(screen, score_game)
        else:
            screen.fill("black")
            start_screen(screen)
        pygame.display.flip()
    pygame.quit()
