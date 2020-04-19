import pygame
import random
import numpy
import algorithms
import heapq
import math
pygame.init()

class scroll(object):
    def __init__(self, position_scroll, position_button, color_scroll, color_button):
        self.position_scroll = position_scroll
        self.position_button = position_button
        self.color_scroll = color_scroll
        self.color_button = color_button
        self.width_scroll = 100
        self.width_button = 10
        self.height_scroll = 15
        self.height_button =15
    def draw(self,surface):
        pygame.draw.rect(surface,self.color_scroll, (self.position_scroll[0], self.position_scroll[1], self.width_scroll, self.height_scroll))
        pygame.draw.rect(surface,self.color_button, (self.position_button[0], self.position_button[1], self.width_button, self.height_button))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if (self.position_scroll[0] <= mouse_pos[0] <= self.position_scroll[0]+self.width_scroll-8 and
           self.position_scroll[1] <= mouse_pos[1] <= self.position_scroll[1]+self.height_scroll and
           mouse_click[0] == 1):
           (x,y) = (mouse_pos[0],self.position_button[1])
           self.position_button = (x,y)
    def speed(self):
        return 1000 -(self.position_button[0] - self.position_scroll[0])*10 + 5

def step(surface):
    global f,r, turn_on_fox, number_of_steps
    if turn_on_fox:
        f.move()
    else:
        r.move()
    turn_on_fox = not turn_on_fox
    number_of_steps += 1

class button(object):
    def __init__(self,position, activeColor, inactiveColor, text):
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
            if self.position[0] < mouse_position[0] < self.position[0]+self.width and self.position[1] < mouse_position[1] < self.position[1]+self.height:
                return True
        return False

    def draw(self,surface):
        cur = pygame.mouse.get_pos()
        #click = pygame.mouse.get_pressed()
        if self.position[0] < cur[0] < self.position[0]+self.width and self.position[1] < cur[1] < self.position[1]+self.height:
            pygame.draw.rect(surface,self.inactiveColor, (self.position[0], self.position[1],self.width,self.height))
        else:
            pygame.draw.rect(surface,self.activeColor, (self.position[0], self.position[1],self.width,self.height))
        textSurface, textRect = text_objects (self.text, (0,0,0))
        textRect.center = (self.position[0]+self.width//2, self.position[1]+self.height//2)
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


def text_objects(text,color):
    font = pygame.font.SysFont(None, 22)
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


class fox(object):
    rows = 25
    width = 500
    rabbit_last_seen = None

    def __init__(self, start, color):
        self.position = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def moveHelp(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position = (self.position[0] + dirnx, self.position[1] + dirny)

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
        '''
        if (r.position[1], self.position[1]) in {(0, 1), (24, 23)} and abs(self.position[0] - r.position[0]) == 1:
            self.position = r.position
        if (r.position[0], self.position[0]) in {(0, 1), (24, 23)} and abs(self.position[1] - r.position[1]) == 1:
            self.position = r.position
        '''
        if algorithms.see_each_other(self.position, r.position, position_matrix):
            path= algorithms.minimal_distance(self.position, r.position, position_matrix)
            self.position = path[-1]
            self.rabbit_last_seen = r.position
        elif self.rabbit_last_seen != None and self.rabbit_last_seen != self.position:
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
    fox_last_seen = None
    prev_position = None

    def __init__(self, start, color):
        self.position = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    #def moveHelp(self, dirnx, dirny):
    #    self.dirnx = dirnx
    #   self.dirny = dirny
    #    self.position = (self.position[0] + dirnx, self.position[1] + dirny)

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
        if algorithms.see_each_other(self.position, f.position, position_matrix):
            self.fox_last_seen = f.position
        if self.fox_last_seen != None:
            options = []
            for (dx,dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                curr_position = (self.position[0] + dx, self.position[1] + dy)
                if outOffBoundaries(curr_position) or isCollision(curr_position):
                    continue
                if curr_position == self.prev_position:
                    continue
                if algorithms.distance(f.position, curr_position) == 1  or curr_position == f.position:
                    continue
                curr_cost = algorithms.f(12 - (abs(curr_position[0] - self.fox_last_seen[0]) + abs(curr_position[1] - self.fox_last_seen[1])))
                curr_cost += algorithms.f(curr_position[0] - 12) + algorithms.f(curr_position[1] - 12)
                if curr_position[0] in [0,1,24,23] or curr_position[0] in [0,1,24,23]:
                    curr_cost += 30
                
                heapq.heappush(options, (curr_cost, curr_position)) 

            tmp = self.prev_position
            self.prev_position = self.position
            if options == []:
                self.position = tmp
            else:
                self.position = heapq.heappop(options)[1]
        else:
            options = []
            for (dx, dy) in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                curr_position = (self.position[0] + dx, self.position[1] + dy)
                if outOffBoundaries(curr_position) or isCollision(curr_position):
                    continue
                options.append(curr_position)
            self.position = random.choice(options)
            

        self.turn += 1


def drawGrid(width, rows, surface):
    sizeBtwn = width // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))
    pygame.draw.rect(surface,(255,255,255),(0,500,500,200))


def bushCoord(density):
    global position_matrix
    coords = []
    while density>0:
        x = random.randrange(0, 25)
        y = random.randrange(0, 25)
        if position_matrix[x][y] == 0 :
            coords.append((x, y))
            position_matrix[x][y] = 1
            density -= 1
    return coords



def spawnBush(surface, coords):
    global bush
    for coord in coords:
        b = bush(coord, (0, 255, 0))
        b.draw(surface)


def refreshWindow(surface, coords):
    global s, rows, width, f, r, bStart, bRun, bStop, bStep, bReplay
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    spawnBush(surface, coords)
    f.draw(surface, True)
    r.draw(surface, True)
    s.draw(surface)
    textSurface, textRect = text_objects ("Speed", (0,0,0))
    textRect.center = (50,533)
    surface.blit(textSurface, textRect)    
    for b in buttons:
        b.draw(surface)
    pygame.display.update()





def main():
    global s, coords, rows, width, f, r, position_matrix, bStart, bRun, bStop, bStep, bReplay, buttons, turn_on_fox, number_of_steps
    rows = 25
    width = 500
    position_matrix = numpy.zeros((rows+1, rows+1))
    field = pygame.display.set_mode((width, 560))
    game = True
    f = fox((10, 10), (255, 51, 0))
    r = rabbit((12, 15), (255, 255, 255))
    bStart = button((200,520), (210,210,210), (160,160,160), "Start")
    bRun = button((260,520), (210,210,210), (160,160,160), "Run")
    bStop = button((320,520), (210,210,210), (160,160,160), "Stop")
    bStep = button((380,520), (210,210,210), (160,160,160), "Step")
    bReplay = button((440,520), (210,210,210), (160,160,160), "Replay")
    buttons = [bStart, bRun, bStop, bStep, bReplay]
    s = scroll((80,525),(170,525), (180,180,180),(130,130,130))
    clock = pygame.time.Clock()
    coords = bushCoord(80)
    turn_on_fox = True
    running = False
    number_of_steps = 0

    while game:
        pygame.time.delay(s.speed())
        clock.tick(10)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                step(field)

        if running:
            step(field)        
        if bStep.pressed():
            step(field)
            running = False
        if bStart.pressed():
            running = True
        if bRun.pressed():
            running = True
        if bStop.pressed():
            running = False

        refreshWindow(field, coords)

        if (f.position == r.position) or r.turn == 500:
            print(number_of_steps)
            game = False
        
main()
