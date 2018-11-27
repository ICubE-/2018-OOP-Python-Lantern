import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("상!평!")

x=50
y=50
width=40
height=60
vel=5

isJump=False
jumpCount=10

def redrawGameWindow():
    win.blit(bg,(0,0))

#mainloop
run = True
while run:
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x>0:
        x-=vel

    if keys[pygame.K_RIGHT] and x<500-width-vel:
        x+=vel

    if not (isJump):
        if keys[pygame.K_UP] and y>0:
            y-=vel

        if keys[pygame.K_DOWN] and y<500-height-vel:
            y+=vel

        if keys[pygame.K_SPACE]:
            isJump = True

    else:
        if jumpCount >= -10:
            neg=1
            if jumpCount < 0:
                neg=-1
            y-=(jumpCount **2)/2*neg
            jumpCount -=1
        else:
            isJump =False
            jumpCount = 10

    win.fill((0,0,0))
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))
    pygame.display.update()
pygame.quit()