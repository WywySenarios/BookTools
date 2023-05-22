import pygame
import os
import re

pygame.init()

screen = pygame.display.set_mode((800, 800), 0)
clock = pygame.time.Clock()
running = True
status = 0
scroll = 0
# 0 for menu, 1 for scroll

items = {}
keys = list(items.keys())


def analyze(data):
    global items
    global keys  # only need to update keys here because when keys are used this function always runs.
    items = {}
    data = open("texts/" + data, "rb")
    data = data.read()
    data = data.decode("UTF-8")
    splice = re.findall("[a-zA-Z]+'?[a-zA-Z]*", data)
    for x in splice:
        x = x.lower()
        if items.get(x) == None:
            items[x] = 1
        else:
            items[x] += 1
    keys = list(items.keys())
    keys.sort()


def startup():
    global files
    files = os.listdir("texts")
    mainscreen()


def mainscreen():
    global status, scroll
    status = 0
    scroll = 0
    mainscreenupdate()


def mainscreenupdate():
    button = pygame.image.load("files/button.png")
    buttonRect = button.get_rect()
    for x in range(scroll, 5 + scroll):
        screen.blit(button, (0, x * 160), buttonRect)
        try:
            if 760 * 0.75 / (len(files[x]) - 3) > 120 * 0.75:
                font = pygame.font.SysFont('Verdana', int(120 * 0.75))
            else:
                font = pygame.font.SysFont('Verdana', int(760 * 0.75 / (len(files[x]) - 3)))  # length 10
            sending = font.render(files[x][:-4], False, (0, 0, 0))
            screen.blit(sending, (20, x * 160 + 5))
        except:
            pass
    pygame.display.flip()


def textscreen():
    global status, scroll
    status = 1
    scroll = 0
    textscreenupdate()


def textscreenupdate():
    button = pygame.image.load("files/button.png")
    buttonRect = button.get_rect()
    for x in range(scroll, 5 + scroll):
        screen.blit(button, (0, (x - scroll) * 160), buttonRect)
        try:
            stringy = keys[x] + ": " + str(items[keys[x]])
            if 760 * 0.75 / len(stringy) > 70:
                font = pygame.font.SysFont('Verdana', 90)
            else:
                font = pygame.font.SysFont('Verdana', int(760 * 0.75 / (len(stringy) - 3)))  # length 10
            sending = font.render(stringy, False, (0, 0, 0))
            screen.blit(sending, (20, (x - scroll) * 160 + 5))
        except:
            pass
    pygame.display.flip()



startup()

while running:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                startup()
            elif event.key == pygame.K_UP:
                if scroll > 0:
                    scroll -= 1
                    if status == 0:
                        mainscreenupdate()
                    else:
                        textscreenupdate()
            elif event.key == pygame.K_DOWN:
                if status == 0: # need to make sure I can't scroll down to extremes later.
                    scroll += 1
                    mainscreenupdate()
                else:
                    scroll += 1
                    textscreenupdate()
            elif event.key == pygame.K_ESCAPE:
                mainscreen()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if status == 0:
                try:
                    analyze(files[int(pygame.mouse.get_pos()[1] / 160) + scroll])
                    textscreen()
                except:
                    continue
            else:
                try:
                    keys.pop(int(pygame.mouse.get_pos()[1] / 160) + scroll)
                    textscreenupdate()
                except:
                    continue
