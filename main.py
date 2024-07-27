import pygame
from sys import exit
import random
import time

pygame.init()

width = 1400
height = 669
screen = pygame.display.set_mode((width, height))

#set game title
pygame.display.set_caption('Le Chat Paresseux')

#declare clock in order to limit frames/sec
clock = pygame.time.Clock()

#text
text_font = pygame.font.Font('img/GloriousChristmas-BLWWB.ttf', 40)

#test_surface = pygame.Surface((100, 200))
#test_surface.fill('greenyellow')
#rect = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(60, 60, 60, 60))

sky_surface = pygame.image.load('img/bigsky.jpeg')
text_surface = text_font.render('Le Chat Paresseux', False, 'Black')
winthegame_surface = text_font.render('YOU WON !!!', True, 'Black')
kitty_surface = pygame.image.load('img/kittenTrans50.png')
cat_surface = pygame.image.load('img/cat50.png')
ground_surface = pygame.image.load('img/ground50.jpeg')
brick_surface = pygame.image.load('img/brick50.jpeg')

stop = False
while stop == False:
    nbRangee = input("Combien de bloques par rangée (3-10)? ")
    nbRangee = int(nbRangee)
    if nbRangee > 2 and nbRangee < 11:
        stop = True

        #debut position briques
        brick_rect = brick_surface.get_rect(topleft = (700-(50*nbRangee + 5*nbRangee-1)/2, 335-(50*nbRangee + 5*nbRangee-1)/2))

        #debut position titre
        text_rect = text_surface.get_rect(center = (700, (335-(50*nbRangee + 5*nbRangee-1)/2)/2 + 10))

        #position winning text
        winthegame_rect = text_surface.get_rect(topleft = (900, 500))


        #pour positionner chat
        randint1 = random.randrange(0, nbRangee)
        randint2 = random.randrange(0, nbRangee)
        cat_rect = cat_surface.get_rect(topleft = (700-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint1, 335-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint1))
        print("cat_rect.x ", cat_rect.x)
        print("cat_rect.y ", cat_rect.y)

        listofx = []
        listofy = []
        posx = 100
        posy = 100

        for y in range(nbRangee):
            for x in range(nbRangee):
                if brick_rect.x not in listofx:
                    listofx.append(brick_rect.x)
                brick_rect.x += 55
            brick_rect.x = 700-(50*nbRangee + 5*nbRangee-1)/2
            listofy.append(brick_rect.y)
            brick_rect.y += 55

        print("listofx ", listofx)
        print("listofy ", listofy)

        while True:
            
            #block image transfer (put one surface on another)
            screen.blit(sky_surface, (0, 0))
            screen.blit(text_surface, text_rect)
            screen.blit(cat_surface, cat_rect)

            brick_rect.x = 700-(50*nbRangee + 5*nbRangee-1)/2
            brick_rect.y = 335-(50*nbRangee + 5*nbRangee-1)/2

            for y in range(nbRangee):
                for x in range(nbRangee):
                    if x != posx or y != posy:
                        screen.blit(brick_surface, (brick_rect.x, brick_rect.y))
                    brick_rect.x += 55
                brick_rect.x = 700-(50*nbRangee + 5*nbRangee-1)/2
                brick_rect.y += 55

        # list of events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # when player clicks on a square, reveal what is under
                if event.type == pygame.MOUSEBUTTONUP:
                    mousex, mousey = pygame.mouse.get_pos()
                    posx = len(listofx)-1
                    posy = len(listofy)-1
                    
                    for x in range(len(listofx)-1):
                        if mousex >= listofx[x] and mousex < listofx[x+1]:
                            posx = x
                            break
                        
                    for y in range(len(listofy)-1):
                        if mousey >= listofy[y] and mousey < listofy[y+1]:
                            posy = y
                            break

                    if posx == listofx.index(cat_rect.x) and posy == listofy.index(cat_rect.y):
                        nbRangee = 0
                        stop = False
                        print("YOU WON")
                        break
                        # while stop == False:
                        #     screen.blit(winthegame_surface, winthegame_rect)
                        #     pygame.display.update()
                        #     clock.tick(60)

            pygame.display.update()

            #max 60 frames/sec
            clock.tick(60)
