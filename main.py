import pygame

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

running = True

# plain surface
surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100

#importing an image
player_surf = pygame.image.load('/home/dalek/shark-kitty/assets/images/DurrrSpaceShip.png')
while running:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw the game
    screen.fill('#282828')
    x += 0.1
    screen.blit(player_surf,(x,150))
    #actual draw
    pygame.display.flip()

pygame.quit()