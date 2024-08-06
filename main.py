import pygame
from sys import exit
import random
import time

pygame.init()

width = 1400
height = 669
screen = pygame.display.set_mode((width, height))

#set game title
pygame.display.set_caption('The Lazy Cat')

#declare clock in order to limit frames/sec
clock = pygame.time.Clock()

#text
text_font = pygame.font.Font('img/GloriousChristmas-BLWWB.ttf', 40)
sm_font = pygame.font.Font('img/GloriousChristmas-BLWWB.ttf', 20)
score = 0
gameHistory = []

#colors
palepink = '#F4DDD0'
pink = '#E8BBCF'
darkpurple = '#0F2268'

#space settings
border = 20
line_spacing = 10
font_height = text_font.get_height()
sm_height = sm_font.get_height()


#test_surface = pygame.Surface((100, 200))
#test_surface.fill('greenyellow')
#rect = pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(60, 60, 60, 60))

sky_surface = pygame.image.load('img/bigsky.jpeg')
text_surface = text_font.render('The Lazy Cat', False, palepink)
score_surface = text_font.render('Moves : ', False, 'Black')
scorenum_surface = text_font.render(str(score), False, 'Black')
lines = ["\t\t\tGame History", "\t\t\tRows\t\tMoves"]
chooseRows_surface = text_font.render('How many blocks per row (3-10)? ', False, 'Black')
winthegame_surface = text_font.render('YOU WON !!! click anywhere to start a new game', False, 'Black')
kitty_surface = pygame.image.load('img/kittenTrans50.png')
cat_surface = pygame.image.load('img/cat50.png')
ground_surface = pygame.image.load('img/ground50.jpeg')
brick_surface = pygame.image.load('img/brick50.jpeg')
refresh_surface = text_font.render('Refresh', False, 'Black')
quit_surface = text_font.render('Quit', False, 'Black')
chatouter_surface = pygame.Surface((200+line_spacing, 400+line_spacing))
chatouter_surface.fill('Black')
chatinner_surface = pygame.Surface((200, 400))
chatinner_surface.fill(darkpurple)
chattitle_surface = sm_font.render('Chatroom', False, pink)

score_rect = score_surface.get_rect(topright = (width - border, border))
refresh_rect = refresh_surface.get_rect(bottomright = (width-border, height-border-quit_surface.get_height()))
quit_rect = quit_surface.get_rect(bottomright = (width-border, height-border))
chatouter_rect = chatouter_surface.get_rect(topright = (width-border+line_spacing/2, 20+2*(score_surface.get_height() + line_spacing)-line_spacing/2))
chatinner_rect = chatinner_surface.get_rect(topright = (width-20, 20+2*(score_surface.get_height() + line_spacing)))
chattitle_rect = chattitle_surface.get_rect(center = (width-20-chatinner_surface.get_width()/2, border+2*(score_surface.get_height() + line_spacing) + line_spacing))


kittyFactor = [-1, 0, 1]
groundFactor = [-2, -1, 0, 1, 2]

def display_background(nbRangee):
    screen.blit(sky_surface, (0, 0))
    text_rect = text_surface.get_rect(center = (width/2, ((height-(50*nbRangee + 5*nbRangee-1))/2)/2))
    for i, line in enumerate(lines):
        htitle_surface = sm_font.render(line, True, 'Black')
        htitle_rect = htitle_surface.get_rect(topleft = (20, 20 + i*(htitle_surface.get_height() + line_spacing)))
        screen.blit(htitle_surface, htitle_rect)
    screen.blit(text_surface, text_rect)
    screen.blit(text_surface, text_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(refresh_surface, refresh_rect)
    screen.blit(quit_surface, quit_rect)
    screen.blit(chatouter_surface, chatouter_rect)
    screen.blit(chatinner_surface, chatinner_rect)
    screen.blit(chattitle_surface, chattitle_rect)

    for i, record in enumerate(gameHistory):
        # history_text = f"{i+1}. \t\t\t\t{record['nbRangee']} \t\t\t\t\t\t{record['score']}"
        historynum_surface = sm_font.render(f"{i+1}.", False, 'Black')                            
        historynum_rect = historynum_surface.get_rect(topleft = (border, border + 2*(sm_height + line_spacing) + i*historynum_surface.get_height()))
        historyrow_surface = sm_font.render(f"{record['nbRangee']}", False, 'Black')   
        historyrow_rect = historynum_surface.get_rect(topleft = (70, border + 2*(sm_height + line_spacing) + i*historyrow_surface.get_height()))
        historyscore_surface = sm_font.render(f"{record['score']}", False, 'Black')   
        historyscore_rect = historyscore_surface.get_rect(topleft = (145, 20 + 2*(sm_height + line_spacing) + i*historyscore_surface.get_height()))
        screen.blit(historynum_surface, historynum_rect)
        screen.blit(historyrow_surface, historyrow_rect)
        screen.blit(historyscore_surface, historyscore_rect)

def display_surround(multiplier, surface, minX, minY, maxX, maxY) -> list[any]:
    array = []
    for i in range(len(multiplier)):
        for j in range(len(multiplier)):
            if i == 0 or i == len(multiplier)-1 or j == 0 or j == len(multiplier)-1:
                if (cat_rect.x + 55*multiplier[i]) >= minX and (cat_rect.x + 55*multiplier[i]) <= maxX and (cat_rect.y + 55*multiplier[j]) >= minY and (cat_rect.y + 55*multiplier[j]) <= maxY :
                    rect = surface.get_rect(topleft = (cat_rect.x + 55*multiplier[i], cat_rect.y + 55*multiplier[j]))
                    array.append(rect)
    return array

def check_reset(mousex, mousey, nbRangee):
    global gameHistory
    global score
    global stop
    if mousex >= 1230 and mousex <= 1375 and mousey >= 575 and mousey <= 600 :
        #popup ?
        gameHistory = []
        score = 0
        display_background(nbRangee)
        stop = False

def check_quit(mousex, mousey):
    if mousex >= 1300 and mousex <= 1375 and mousey >= 615 and mousey <= 650 :
        #popup ?
        pygame.quit()
        exit()

while True:
    
    #block image transfer (put one surface on another)
    display_background(3)

    #game question
    chooseRows_rect = chooseRows_surface.get_rect(center = (width/2, height/2))

    #score
    scorenum_rect = scorenum_surface.get_rect(topright = (width - 80, 60))

    stop = False
    while stop == False:
        screen.blit(chooseRows_surface, chooseRows_rect)
        nbRangee = "0"

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                nbRangee += event.unicode

            if event.type == pygame.MOUSEBUTTONUP: 
                mousex, mousey = pygame.mouse.get_pos()
                check_reset(mousex, mousey, 3)
                check_quit(mousex, mousey)

                
        nbRangee = int(nbRangee)
        
        #position winning text
        winthegame_rect = winthegame_surface.get_rect(center = (width/2, (50*nbRangee + 5*nbRangee-1)+(height-(50*nbRangee + 5*nbRangee-1))/2 + (height-(50*nbRangee + 5*nbRangee-1))/2/2))
    
        if nbRangee > 2 and nbRangee < 11:
            minX = width/2-(50*nbRangee + 5*nbRangee-1)/2
            minY = height/2-(50*nbRangee + 5*nbRangee-1)/2
            maxX = width/2+(50*nbRangee + 5*nbRangee-1)/2
            maxY = height/2+(50*nbRangee + 5*nbRangee-1)/2
            brick_rect = brick_surface.get_rect(topleft = (minX, minY))
            
            #positionn cat
            randint1 = random.randrange(0, nbRangee)
            randint2 = random.randrange(0, nbRangee)
            cat_rect = cat_surface.get_rect(topleft = (width/2-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint1, height/2-(50*nbRangee + 5*nbRangee-1)/2 + 55*randint2))

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
                brick_rect.x = width/2-(50*nbRangee + 5*nbRangee-1)/2
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

                                mousex, mousey = pygame.mouse.get_pos()
                                check_reset(mousex, mousey, nbRangee)
                                check_quit(mousex, mousey)
                                    
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
                        
                        check_reset(mousex, mousey, nbRangee)
                        check_quit(mousex, mousey)


                pygame.display.update()

                #max 60 frames/sec
                clock.tick(60)

        pygame.display.update()

        #max 60 frames/sec
        clock.tick(60)

    pygame.display.update()

    #max 60 frames/sec
    clock.tick(60)
