import pygame
import random
import numpy
pygame.init()

def step(surface):
    global bStart, bRun, bStop, bStep, bReplay, coords,f,r
    bStart.pressed = False
    while bStep.pressed:
        bStep.pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        f.move()
        r.move()
        refreshWindow(surface, coords)

def pause(surface):
    global bStart, bRun, bStop, bStep, bReplay, coords
    bStop.pressed = True
    bStart.pressed = False
    while bStop.pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        refreshWindow(surface, coords)
        if bStart.pressed == True:
            bStop.pressed = False

class button(object):
    def __init__(self,position, activeColor, inactiveColor, text):
        self.position = position
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.text = text
        self.pressed = False

    def draw(self,surface):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.position[0] < cur[0] < self.position[0]+55 and self.position[1] < cur[1] < self.position[1]+25:
            pygame.draw.rect(surface,self.inactiveColor, (self.position[0], self.position[1],55,25))
            if click[0]==1:
                if self.text == "Start":
                    self.pressed = True
                elif self.text == "Stop":
                    pause(surface)
                    self.pressed = False
                elif self.text == "Step":
                    self.pressed = True
                    step(surface)
        else:
            pygame.draw.rect(surface,self.activeColor, (self.position[0], self.position[1],55,25))
        textSurface, textRect = text_objects (self.text, (0,0,0))
        textRect.center = (self.position[0]+55//2, self.position[1]+25//2)
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

def isCollision(cord1):
    global position_matrix
    if position_matrix[cord1[0]][cord1[1]] :
        return True
    return False

def outOffBoundaries(x1,y1):
    if x1<0 or x1>24 or y1<0 or y1>24:
        return True
    return False


class fox(object):
    rows = 25
    width = 500

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        dirnx = 0
        dirny = 0
        while dirnx == 0 and dirny == 0:
            dirnx = random.randrange(-1, 2)
            if dirnx == 0:
                dirny = random.randrange(-1, 2)
            if isCollision((self.position[0] + dirnx, self.position[1] + dirny)) :
                dirnx = 0
                dirny = 0
            if outOffBoundaries(self.position[0] + dirnx, self.position[1] + dirny):
                dirnx = 0
                dirny = 0
        self.moveHelp(dirnx, dirny)

class rabbit(object):
    rows = 25
    width = 500
    turn = 0

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
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            center = dis // 2
            radius = 3
            circleMiddle = (i * dis + center - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        dirnx = 0
        dirny = 0
        while dirnx == 0 and dirny == 0:
            dirnx = random.randrange(-1, 2)
            if dirnx == 0:
                dirny = random.randrange(-1, 2)
            if isCollision((self.position[0] + dirnx, self.position[1] + dirny)) :
                dirnx = 0
                dirny = 0
            if outOffBoundaries(self.position[0] + dirnx, self.position[1] + dirny):
                dirnx = 0
                dirny = 0
        self.moveHelp(dirnx, dirny)
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
        if position_matrix[x][y]==0 :
            coords.append((x, y))
            position_matrix[x][y] = 1
            density-=1
    return coords



def spawnBush(surface, coords):
    global bush
    for coord in coords:
        b = bush(coord, (0, 255, 0))
        b.draw(surface)


def refreshWindow(surface, coords):
    global rows, width, f, r, bStart, bRun, bStop, bStep, bReplay
    surface.fill((0,0,0))
    drawGrid(width, rows, surface)
    spawnBush(surface, coords)
    f.draw(surface, True)
    r.draw(surface, True)
    bStart.draw(surface)
    bRun.draw(surface)
    bStop.draw(surface)
    bStep.draw(surface)
    bReplay.draw(surface)
    pygame.display.update()





def main():
    global coords,rows, width, f, r, position_matrix, bStart, bRun, bStop, bStep, bReplay
    rows = 25
    width = 500
    position_matrix = numpy.zeros((rows+1, rows+1))
    field = pygame.display.set_mode((width, 560))
    game = True
    f = fox((10, 10), (255, 51, 0))
    r = rabbit((12, 13), (255, 255, 255))
    bStart = button((200,520), (210,210,210), (160,160,160), "Start")
    bRun = button((260,520), (210,210,210), (160,160,160), "Run")
    bStop = button((320,520), (210,210,210), (160,160,160), "Stop")
    bStep = button((380,520), (210,210,210), (160,160,160), "Step")
    bReplay = button((440,520), (210,210,210), (160,160,160), "Replay")
    clock = pygame.time.Clock()
    coords = bushCoord(50)
    while game:
        pygame.time.delay(100)
        clock.tick(10)
        if (f.position == r.position) or r.turn == 10000:
            pygame.quit()
        f.move()
        r.move()
        refreshWindow(field, coords)


main()
