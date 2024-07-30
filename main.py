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
sm_font = pygame.font.Font('img/GloriousChristmas-BLWWB.ttf', 20)
score = 0
gameHistory = []

#test_surface = pygame.Surface((100, 200))
#test_surface.fill('greenyellow')
#rect = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(60, 60, 60, 60))

sky_surface = pygame.image.load('img/bigsky.jpeg')
text_surface = text_font.render('Le Chat Paresseux', False, 'Black')
score_surface = text_font.render('Score : ', False, 'Black')
scorenum_surface = text_font.render(str(score), False, 'Black')
htitle_surface = sm_font.render('Game History', True, 'Black')
chooseRows_surface = text_font.render('How many blocks per row (3-10)? ', False, 'Black')
winthegame_surface = text_font.render('YOU WON !!! click anywhere to start a new game', False, 'Black')
kitty_surface = pygame.image.load('img/kittenTrans50.png')
cat_surface = pygame.image.load('img/cat50.png')
ground_surface = pygame.image.load('img/ground50.jpeg')
brick_surface = pygame.image.load('img/brick50.jpeg')

kittyFactor = [-1, 0, 1]
groundFactor = [-2, -1, 0, 1, 2]

def display_background(nbRangee):
    screen.blit(sky_surface, (0, 0))
    text_rect = text_surface.get_rect(center = (700, (335-(50*nbRangee + 5*nbRangee-1)/2)/2 + 10))
    score_rect = score_surface.get_rect(topright = (width - 20, 20))
    htitle_rect = htitle_surface.get_rect(topleft = (20, 20))
    screen.blit(text_surface, text_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(htitle_surface, htitle_rect)


def display_surround(multiplier, surface, minX, minY, maxX, maxY) -> list[any]:
    array = []
    for i in range(len(multiplier)):
        for j in range(len(multiplier)):
            if i == 0 or i == len(multiplier)-1 or j == 0 or j == len(multiplier)-1:
                if (cat_rect.x + 55*multiplier[i]) >= minX and (cat_rect.x + 55*multiplier[i]) <= maxX and (cat_rect.y + 55*multiplier[j]) >= minY and (cat_rect.y + 55*multiplier[j]) <= maxY :
                    rect = surface.get_rect(topleft = (cat_rect.x + 55*multiplier[i], cat_rect.y + 55*multiplier[j]))
                    array.append(rect)
    return array

while True:
    
    #block image transfer (put one surface on another)
    display_background(3)

    #game question
    chooseRows_rect = chooseRows_surface.get_rect(center = (width/2, height/2))

    #score
    scorenum_rect = scorenum_surface.get_rect(topright = (width - 80, 60))

    #position winning text
    winthegame_rect = winthegame_surface.get_rect(center = (700, 575))
    
    stop = False
    while stop == False:
        screen.blit(chooseRows_surface, chooseRows_rect)
        nbRangee = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                nbRangee = event.unicode

        nbRangee = int(nbRangee)

        if nbRangee > 2 and nbRangee < 11:
            minX = 700-(50*nbRangee + 5*nbRangee-1)/2
            minY = 335-(50*nbRangee + 5*nbRangee-1)/2
            maxX = 700+(50*nbRangee + 5*nbRangee-1)/2
            maxY = 335+(50*nbRangee + 5*nbRangee-1)/2
            brick_rect = brick_surface.get_rect(topleft = (minX, minY))
            
            #positionn cat
            randint1 = random.randrange(0, nbRangee)
            randint2 = random.randrange(0, nbRangee)
            cat_rect = cat_surface.get_rect(topleft = (700-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint1, 335-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint2))

            #position kittens
            kittyArray = display_surround(kittyFactor, kitty_surface, minX, minY, maxX, maxY)
            groundArray = display_surround(groundFactor, ground_surface, minX, minY, maxX, maxY)

            #put the x position of the top left corner of each brick in an array
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

            stop = True

            while stop:
                display_background(nbRangee)

                screen.blit(cat_surface, cat_rect)
                for i in range(len(kittyArray)):
                    screen.blit(kitty_surface, kittyArray[i])
                for i in range(len(groundArray)):
                    screen.blit(ground_surface, groundArray[i])
                screen.blit(scorenum_surface, scorenum_rect)

                brick_rect.x = 700-(50*nbRangee + 5*nbRangee-1)/2
                brick_rect.y = 335-(50*nbRangee + 5*nbRangee-1)/2

                for y in range(nbRangee):
                    for x in range(nbRangee):
                        if x != posx or y != posy:
                            screen.blit(brick_surface, (brick_rect.x, brick_rect.y))
                        brick_rect.x += 55
                    brick_rect.x = 700-(50*nbRangee + 5*nbRangee-1)/2
                    brick_rect.y += 55

                if posx == listofx.index(cat_rect.x) and posy == listofy.index(cat_rect.y):
                    gameHistory.append({'nbRangee' : nbRangee, 'score' : score})
                    nbRangee = 0
                    won = True
                    while won:
                        
                        screen.blit(winthegame_surface, winthegame_rect)
                        for i, record in enumerate(gameHistory):
                            history_text = f"Row: {record['nbRangee']}, Score: {record['score']}"
                            history_surface = sm_font.render(history_text, False, 'Black')                            
                            history_rect = history_surface.get_rect(topleft = (20, 40 + i*20))
                            screen.blit(history_surface, history_rect)

                        pygame.display.flip()

                        for event in pygame.event.get():
                            #if player clicks 'ESC', quit the game doesnt work
                            if event.type == pygame.QUIT: # if event.key == pygame.K_ESCAPE: doesnt work
                                pygame.quit()
                                exit()

                            # if player clicks anywhere, start new game
                            if event.type == pygame.MOUSEBUTTONUP:
                                score = 0
                                display_background(nbRangee)
                                stop = False
                                won = False

                        # pygame.display.update()
                        # clock.tick(60)

            # list of events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

            # when player clicks on a square, reveal what is under
                    if event.type == pygame.MOUSEBUTTONUP:
                        score += 1
                        scorenum_surface = text_font.render(str(score), False, 'Black')
                        screen.blit(scorenum_surface, scorenum_rect)
                        pygame.display.flip()

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
            

                pygame.display.update()

                #max 60 frames/sec
                clock.tick(60)

        pygame.display.update()

        #max 60 frames/sec
        clock.tick(60)

    pygame.display.update()

    #max 60 frames/sec
    clock.tick(60)
