import pygame
import sys
import random

colors = [
    (0, 0, 0),
    (127, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
    (255, 128, 0),
    (0, 0, 255),
    (128, 255, 0),
    (51, 255, 255)
]


class Tetromino:  # pieces
    x = 0
    y = 0

    # Each list of lists is a piece
    tetrom = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
        [[1, 2, 6, 7], [2, 5, 6, 9]],
        [[1, 2, 4, 5], [1, 5, 6, 10]]
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrom) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.tetrom[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetrom[self.type])


class Tetris:
    level = 2
    score = 0
    state = "start"
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    tetrom = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_tetrom(self):
        self.tetrom = Tetromino(5, 0)

    def intersects(self):  # check if tetromino is intersecting with the field or other pieces
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrom.image():
                    if i + self.tetrom.y > self.height - 1 or \
                            j + self.tetrom.x > self.width - 1 or \
                            j + self.tetrom.x < 0 or \
                            self.field[i + self.tetrom.y][j + self.tetrom.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 3

    def clean_grid(self):
        self.score = 0
        for i in range(self.height):
            for j in range(self.width):
                self.field[i][j] = 0


    def go_space(self):
        while not self.intersects():
            self.tetrom.y += 1
        self.tetrom.y -= 1
        self.freeze()

    def go_down(self):
        self.tetrom.y += 1
        if self.intersects():
            self.tetrom.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.tetrom.x
        self.tetrom.x += dx
        if self.intersects():
            self.tetrom.x = old_x

    def rotate(self):
        old_rotate = self.tetrom.rotation
        self.tetrom.rotate()
        if self.intersects():
            self.tetrom.x = old_rotate

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrom.image():
                    self.field[i + self.tetrom.y][j + self.tetrom.x] = self.tetrom.color
        self.break_lines()
        self.new_tetrom()
        if self.intersects():
            self.state = "gameover"


# pygame stuff
pygame.init()

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

size = (400, 500)  # window size
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps = 30


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    screen.blit(label, [0, 0])


def main():
    pygame.display.set_caption("Testris")
    game = Tetris(20, 10)
    counter = 0
    run = True
    pressing_down = False

    while run:
        if game.tetrom is None:
            game.new_tetrom()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    if game.state == "gameover":
                        game.clean_grid()
                        main_menu()
                    else: main_menu()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(WHITE)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        if game.tetrom is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.tetrom.image():
                        pygame.draw.rect(screen, colors[game.tetrom.color],
                                         [game.x + game.zoom * (j + game.tetrom.x) + 1,
                                          game.y + game.zoom * (i + game.tetrom.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('comicsans', 25, True, False)
        font1 = pygame.font.SysFont('comicsans', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_game_over = font1.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

        screen.blit(text, [0, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])
        pygame.display.flip()
        clock.tick(fps)


def main_menu():
    run = True
    while run:
        screen.fill((0, 0, 0))
        draw_text_middle('Press any button to begin.', 38, (255, 255, 255), screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


main_menu()
