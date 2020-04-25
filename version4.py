import pygame
import random
import numpy
import algorithms
import heapq

pygame.init()


def step(surface):
    global f, r, turn_on_fox, number_of_steps
    number_of_steps += 1
    f.move()
    if f.position == r.position:
        print(number_of_steps)
        winner = "fox"
        return
    pygame.time.delay(100)
    r.move()


class scroll(object):
    def __init__(self, position_scroll, position_button, color_scroll, color_button):
        self.position_scroll = position_scroll
        self.position_button = position_button
        self.color_scroll = color_scroll
        self.color_button = color_button
        self.width_scroll = 100
        self.width_button = 10
        self.height_scroll = 15
        self.height_button = 15

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_scroll,
                         (self.position_scroll[0], self.position_scroll[1], self.width_scroll, self.height_scroll))
        pygame.draw.rect(surface, self.color_button,
                         (self.position_button[0], self.position_button[1], self.width_button, self.height_button))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if (self.position_scroll[0] <= mouse_pos[0] <= self.position_scroll[0] + self.width_scroll - 8 and
                self.position_scroll[1] <= mouse_pos[1] <= self.position_scroll[1] + self.height_scroll and
                mouse_click[0] == 1):
            (x, y) = (mouse_pos[0], self.position_button[1])
            self.position_button = (x, y)

    def speed(self):
        return 1000 - (self.position_button[0] - self.position_scroll[0]) * 10 + 5


class button(object):
    def __init__(self, position, activeColor, inactiveColor, text):
        self.position = position
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.text = text
        self.width = 55
        self.height = 25

    def pressed(self):
        click = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()
        if click[0] == True:
            if self.position[0] < mouse_position[0] < self.position[0] + self.width and self.position[1] < \
                    mouse_position[1] < self.position[1] + self.height:
                return True
        return False

    def draw(self, surface):
        cur = pygame.mouse.get_pos()
        # click = pygame.mouse.get_pressed()
        if self.position[0] < cur[0] < self.position[0] + self.width and self.position[1] < cur[1] < self.position[
            1] + self.height:
            pygame.draw.rect(surface, self.inactiveColor, (self.position[0], self.position[1], self.width, self.height))
        else:
            pygame.draw.rect(surface, self.activeColor, (self.position[0], self.position[1], self.width, self.height))
        textSurface, textRect = text_objects(self.text, (0, 0, 0))
        textRect.center = (self.position[0] + self.width // 2, self.position[1] + self.height // 2)
        surface.blit(textSurface, textRect)


class bush(object):
    rows = 25
    width = 500

    def __init__(self, position, color=(0, 255, 0)):
        self.position = position
        self.color = color

    def draw(self, surface):
        dis = width // rows
        i = self.position[0]
        j = self.position[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


def text_objects(text, color, size="small"):
    if size == "small":
        font = pygame.font.SysFont("comicsansms", 22)
    elif size == "medium":
        font = pygame.font.SysFont("comicsansms", 27)
    else:
        font = pygame.font.SysFont("comicsansms", 37)
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def isCollision(coord):
    global position_matrix
    if position_matrix[coord[0]][coord[1]] == 1:
        return True
    return False


def outOffBoundaries(coord):
    if coord[0] < 0 or coord[0] > 24 or coord[1] < 0 or coord[1] > 24:
        return True
    return False


def number_of_bush_neighbours(position):
    global position_matrix
    sol = 0
    for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
        curr_position = (position[0] + dx, position[1] + dy)
        if outOffBoundaries(curr_position):
            continue
        if isCollision(curr_position):
            sol += 1
    return sol


class fox(object):
    rows = 25
    width = 500
    rabbit_last_seen = None

    def __init__(self, start, color):
        self.position = start
        self.prev_steps = []
        self.color = color

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.position[0]
        j = self.position[1]
        pygame.draw.polygon(surface, self.color, [(i * dis + 1, j * dis + 1), (i * dis + 1 + dis, j * dis + 1),
                                                  (i * dis + 1 + dis // 2, j * dis + 1 + dis)])
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 204, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 204, 0), circleMiddle2, radius)

    def move(self):
        self.prev_steps.append(self.position)
        p = random.randrange(0, 1000)

        if p > 10 and algorithms.see_each_other(self.position, r.position, position_matrix):
            path = algorithms.minimal_distance(self.position, r.position, position_matrix)
            self.position = path[-1]
            self.rabbit_last_seen = r.position
        elif p > 10 and self.rabbit_last_seen != None and self.rabbit_last_seen != self.position:
            path = algorithms.minimal_distance(self.position, r.position, position_matrix)
            self.position = path[-1]
        else:
            options = []
            for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                curr_position = (self.position[0] + dx, self.position[1] + dy)
                if outOffBoundaries(curr_position) or isCollision(curr_position):
                    continue
                options.append(curr_position)
            self.position = random.choice(options)


class rabbit(object):
    rows = 25
    width = 500
    turn = 0
    fox_last_seen = []
    prev_steps = []

    def __init__(self, start, color):
        self.position = start
        self.color = color

    def draw(self, surface, eyes=False):
        dis = self.width // self.rows
        i = self.position[0]
        j = self.position[1]
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def move(self):
        self.prev_steps.append(self.position)
        if algorithms.see_each_other(self.position, f.position, position_matrix):
            self.fox_last_seen.append(f.position)
        else:
            if len(self.fox_last_seen) > 0:
                self.fox_last_seen.append(self.fox_last_seen[-1])
            else:
                self.fox_last_seen.append(None)
        if self.fox_last_seen[-1] != None:
            options = []
            for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                curr_position = (self.position[0] + dx, self.position[1] + dy)
                if outOffBoundaries(curr_position) or isCollision(curr_position):
                    continue
                if len(self.prev_steps) > 1 and curr_position == self.prev_steps[-2]:
                    continue
                if algorithms.distance(f.position, curr_position) == 1:
                    continue
                if number_of_bush_neighbours(curr_position) == 3:
                    continue
                # ??????
                '''
                curr_cost = algorithms.f(12 - (abs(curr_position[0] - self.fox_last_seen[0]) + abs(
                    curr_position[1] - self.fox_last_seen[1])))
                curr_cost += algorithms.f(curr_position[0] - 12) + algorithms.f(curr_position[1] - 12)
                curr_cost-=20*number_of_bush_neighbours(curr_position)
                if curr_position[0] in [0, 1, 24, 23] or curr_position[1] in [0, 1, 24, 23]:
                    curr_cost += 30
                '''
                dist_from_fox = abs(curr_position[0] - self.fox_last_seen[-1][0]) + abs(
                    curr_position[1] - self.fox_last_seen[-1][1])
                curr_cost = algorithms.f(12 - dist_from_fox)
                curr_cost += 5 * algorithms.f(abs(curr_position[0] - 12)) + algorithms.f(abs(curr_position[1] - 12))
                # curr_cost -= 20 * number_of_bush_neighbours(curr_position)
                curr_cost -= 10 * self.number_of_good_bushes()

                if self.fox_last_seen[-1] != None:
                    if not algorithms.see_each_other(curr_position, self.fox_last_seen[-1], position_matrix):
                        curr_cost -= 100
                heapq.heappush(options, (curr_cost, curr_position))

            if options == []:
                self.position = self.prev_steps[-2]
            else:
                self.position = heapq.heappop(options)[1]
        else:
            options = []
            for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                curr_position = (self.position[0] + dx, self.position[1] + dy)
                if outOffBoundaries(curr_position) or isCollision(curr_position):
                    continue
                if number_of_bush_neighbours(curr_position) == 3:
                    continue
                if curr_position == self.position:
                    continue
                options.append(curr_position)
            self.position = random.choice(options)

        self.turn += 1

    def number_of_good_bushes(self):
        sol = 0
        for bush in good_bushes:
            if algorithms.manhattan_distance(bush, self.position) < algorithms.manhattan_distance(bush,
                                                                                                  self.fox_last_seen[
                                                                                                      -1]):
                sol += 1
        return sol


def drawGrid(width, rows, surface):
    sizeBtwn = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))
    pygame.draw.rect(surface, (255, 255, 255), (0, 500, 500, 200))


def bushCoord(density):
    global position_matrix, good_bushes
    bush_coords = []
    while density > 0:
        x = random.randrange(0, 25)
        y = random.randrange(0, 25)
        if position_matrix[x][y] == 0 and (x, y) not in [f.position, r.position]:
            bush_coords.append((x, y))
            position_matrix[x][y] = 1
            density -= 1

    good_bushes = []
    for bush in bush_coords:
        if bush[0] not in {0, 24} and bush[1] not in {0, 24}:
            good_bushes.append(bush)
    return bush_coords


def draw_bushes(surface, bush_coords):
    global bush
    for coord in bush_coords:
        b = bush(coord, (0, 255, 0))
        b.draw(surface)


def refreshWindow(surface, bush_coords):
    global s, rows, width, f, r, bReplay, bRun, bStop, bStep, bReset, number_of_steps
    surface.fill((0, 0, 0))
    drawGrid(width, rows, surface)
    draw_bushes(surface, bush_coords)
    f.draw(surface, True)
    r.draw(surface, True)
    s.draw(surface)
    textSurface, textRect = text_objects("Speed", (0, 0, 0))
    textRect.center = (30, 533)
    surface.blit(textSurface, textRect)
    textSurface, textRect = text_objects("Step: " + str(number_of_steps), (0, 0, 0), "medium")
    textRect.center = (455, 565)
    surface.blit(textSurface, textRect)
    for b in buttons:
        b.draw(surface)
    pygame.display.update()


def message_to_screen(surface, surface_size, text, color, y_displace=0, size="small"):
    textSurface, textRect = text_objects(text, color, size)
    textRect.center = (surface_size[0] // 2, surface_size[1] // 2 + y_displace)
    surface.blit(textSurface, textRect)


def set_table():
    global f, r, bush_coords, good_bushes
    f = fox((random.randrange(3, 20), random.randrange(3, 20)), (255, 51, 0))
    (f_x, f_y) = f.position
    options = [(f_x + i, f_y + 7 - i) for i in range(8)]
    options += [(f_x - i, f_y + 7 - i) for i in range(8)]


    r_pos = random.choice(options)
    while outOffBoundaries(r_pos):
        r_pos = random.choice(options)

    r = rabbit(r_pos, (255, 255, 255))
    bush_coords = bushCoord(50)


def main():
    global good_bushes, s, bush_coords, rows, width, f, r, position_matrix, bReplay, bRun, bStop, bStep, bReplay, buttons, turn_on_fox, number_of_steps
    rows = 25
    width = 500
    position_matrix = numpy.zeros((rows + 1, rows + 1))
    field = pygame.display.set_mode((width, 580))
    game = True
    bRun = button((200, 520), (210, 210, 210), (160, 160, 160), "Run")
    bStop = button((260, 520), (210, 210, 210), (160, 160, 160), "Stop")
    bStep = button((320, 520), (210, 210, 210), (160, 160, 160), "Step")
    bReset = button((380, 520), (210, 210, 210), (160, 160, 160), "Reset")
    bReplay = button((440, 520), (210, 210, 210), (160, 160, 160), "Replay")
    buttons = [bRun, bStop, bStep, bReset, bReplay]
    s = scroll((60, 525), (150, 525), (180, 180, 180), (130, 130, 130))
    clock = pygame.time.Clock()
    set_table()
    turn_on_fox = True
    running = False
    number_of_steps = 0
    winner = None
    gameOver = False

    # endScreen_width = 500
    # endScreen_height = 560
    # endScreen = pygame.display.set_mode((endScreen_width,endScreen_height))
    while game:
        if (f.position == r.position):
            print(number_of_steps)
            winner = "fox"
            gameOver = True
        if number_of_steps == 200:
            winner = "rabbit"
            gameOver = True

        while gameOver:
            field.fill((0, 0, 0))

            if winner == "fox":
                message_to_screen(field, (500, 560), "GAME OVER", (255, 51, 0), -25, "large")
                message_to_screen(field, (500, 560), "Fox won", (255, 51, 0))
                message_to_screen(field, (500, 560), "Press r to restart or q to quit", (255, 51, 0), 25)
            elif winner == "rabbit":
                message_to_screen(field, (500, 560), "GAME OVER", (0, 255, 0), -25, "large")
                message_to_screen(field, (500, 560), "Rabbit won", (0, 255, 0))
                message_to_screen(field, (500, 560), "Press r to restart or q to quit", (0, 255, 0), 25)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    if event.key == pygame.K_q:
                        pygame.quit()
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

        pygame.time.delay(s.speed())
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if running:
            step(field)
        if bStep.pressed():
            step(field)
            running = False
        if bRun.pressed():
            running = True
        if bStop.pressed():
            running = False
        if bReset.pressed():
            main()
        if bReplay.pressed() and number_of_steps >= 1:
            f.position = f.prev_steps[-1]
            f.prev_steps = f.prev_steps[:-1]
            r.position = r.prev_steps[-1]
            r.prev_steps = r.prev_steps[:-1]
            r.fox_last_seen = r.fox_last_seen[:-1]
            number_of_steps -= 1

        refreshWindow(field, bush_coords)


main()