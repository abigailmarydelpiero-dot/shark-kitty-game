import sys, pygame, random

dt = 0
class Meat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Initialize the Sprite parent class
        self.image = pygame.image.load("good_meat.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
    def update(self):
        self.rect.y += 200 * dt
        if self.rect.y >= (shark_rect.topleft[1] + 170):
            self.kill()
            global happyness
            happyness += 50


pygame.init()

size = width, height = 800, 600

my_font = pygame.font.Font(None, 50)

all_sprites = pygame.sprite.Group()



speed = [2, 2]
black = '#282828'
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#pygame.event.set_grab(True)

gold = 0
age = 0
happyness = 400

get_gold = True

sick = pygame.image.load("good_meat.png").convert_alpha()
sick_rect = sick.get_rect()
sick_rect.topleft = (210, 150) 

shark = pygame.image.load("shark.png").convert_alpha()
shark_rect = shark.get_rect()
shark_rect.topleft = (175, 175) 
shark_rect_start_pos = shark_rect.topleft
shark_sick = False

#meat = Meat(random.randint(100, 200), 100)
#all_sprites.add(meat)

#event loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    #print (pygame.mouse.get_focused())

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            shark_rect.y -=200 * dt
            if get_gold:
                gold += 1
                meat = Meat(random.randint(50, 300), -20)
                all_sprites.add(meat)
                happyness -= 10
                get_gold = False
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            shark_rect.y =shark_rect_start_pos[1]
            get_gold = True
   
    if happyness <= 0:
        sys.exit()

    gold_text = my_font.render(f"Gold - {gold}", True, (255, 255, 255))
    happyness_text = my_font.render(f"Happiness - {happyness}", True, (222, 215, 11))
    
    if (random.randint(0,2) == 1):
            shark_sick = True
            print("IH")
            screen.blit(sick, sick_rect)
    all_sprites.update() 
    
    screen.fill(black)

    screen.blit(shark, shark_rect)
    screen.blit(gold_text, (100, 100)) 
    screen.blit(happyness_text, (100, 200)) 

    all_sprites.draw(screen)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()
