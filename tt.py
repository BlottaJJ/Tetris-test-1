import pygame
import sys
import random

colors = [
    (0,0,0),
    (127, 0 ,255),
    (255, 0, 0),
    (0 , 255, 0),
    (255, 128, 0),
    (0, 0, 255),
    (128, 255, 0),
    (51, 255, 255)
]



class Tetrimino:
    x = 0
    y = 0
    tetrim = [
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
        self.type = random.randint(0, len(self.tetrim) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.tetrim[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation +1) % len(self.tetrim[self.type])

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
    tetrim = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_tetrim(self):
        self.tetrim = Tetrimino(5, 0)


    def intersects(self):   #check if tetrimino is intersecting with the field or other pieces
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrim.image():
                    if i + self.tetrim.y > self.height - 1 or \
                        j + self.tetrim.x > self.width - 1 or \
                        j + self.tetrim.x < 0 or \
                        self.field[i + self.tetrim.y][j + self.tetrim.x] > 0:
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
                lines +=1
                for i1 in range(i, 1, -1):
                     for j in range(self.width):
                         self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 3

    def go_space(self):
        while not self.intersects():
            self.tetrim.y += 1
        self.tetrim.y -= 1
        self.freeze()

    def go_down(self):
        self.tetrim.y += 1
        if self.intersects():
            self.tetrim.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.tetrim.x
        self.tetrim.x += dx
        if self.intersects():
            self.tetrim.x = old_x

    def rotate(self):
        old_rotate = self.tetrim.rotation
        self.tetrim.rotate()
        if self.intersects():
            self.tetrim.x = old_rotate

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetrim.image():
                    self.field[i + self.tetrim.y][j+ self.tetrim.x] = self.tetrim.color
        self.break_lines()
        self.new_tetrim()
        if self.intersects():
            game.state = "gameover"


#pygame stuff, not mine
pygame.init()

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)


size = (400, 500) #window size
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")
done = False
clock = pygame.time.Clock()
fps = 30
game = Tetris(20, 10)
counter = 0

pressing_down = False

while not done:
    if game.tetrim is None:
        game.new_tetrim()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
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
                game.__init__(20, 10)
    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.tetrim is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.tetrim.image():
                    pygame.draw.rect(screen, colors[game.tetrim.color],
                                     [game.x + game.zoom * (j + game.tetrim.x) + 1,
                                      game.y + game.zoom * (i + game.tetrim.y) + 1,
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

pygame.quit()




