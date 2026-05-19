import sys, pygame, random, thorpy as tp

dt = 0
class Meat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Initialize the Sprite parent class
        self.image = pygame.image.load("good_meat.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
    def update(self):
        self.rect.y += 200 * dt
        if self.rect.y >= (shark.rect.topleft[1] + 170):
            self.kill()
            global happyness
            happyness += 50

class Sharkitty(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("shark.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (175, 175) 
        self.rect_start_pos = self.rect.topleft
        self.sick = False
        self.name = "no name :("
    def enter_name(self, event):
        global user_text
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                print(f"Submitted Text: {user_text}")
                self.name = user_text
                user_text = ""
            else:
                user_text += event.unicode



pygame.init()

size = width, height = 800, 600

my_font = pygame.font.Font("/home/dalek/shark-kitty/assets/fonts/JetBrains_Mono/JetBrainsMono-VariableFont_wght.ttf", 30)

all_sprites = pygame.sprite.Group()




black = '#282828'
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#pygame.event.set_grab(True)

def render_text(text, value, color, x, y):
    text_string = f"{text}" + f"{value}" 
    text_display = my_font.render(text_string, True, color)
    screen.blit(text_display, (x, y)) 

#ui - thorpy
tp.init(screen, tp.theme_classic)
my_button = tp.Button("feed")
my_button.center_on('screen')

updater = my_button.get_updater()
gold = 0
age = 0
happyness = 400
user_text = ""
get_gold = True

#meat = Meat(random.randint(100, 200), 100)
#all_sprites.add(meat)
shark = Sharkitty()
all_sprites.add(shark)
#event loop
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT: sys.exit()
    #print (pygame.mouse.get_focused())
        shark.enter_name(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                shark.rect.y -=200 * dt
                if get_gold:
                    gold += 1
                    meat = Meat(random.randint(50, 300), -20)
                    all_sprites.add(meat)
                    happyness -= 10
                    get_gold = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                shark.rect.y =shark.rect_start_pos[1]
                get_gold = True

    

    if happyness <= 0:
        sys.exit()
    
    #gold_text = my_font.render(f"Gold - {gold}", True, (255, 255, 255))
    #happyness_text = my_font.render(f"Happiness - {happyness}", True, (222, 215, 11))
    

    if (random.randint(0,100) == 1):
            shark_sick = True

            #screen.blit(sick, sick_rect)
    all_sprites.update() 
    #Sharkitty.update()
    screen.fill(black)

    #screen.blit(Sharkitty.image, Sharkitty.rect)
    #screen.blit(gold_text, (100, 100)) 
    #screen.blit(happyness_text, (100, 200)) 
    render_text('Gold: ', gold, (255, 255, 0), 100, 100)
    render_text('Happiness: ', happyness, (255, 255, 255), 100 , 150)
    render_text('Name Input: ', user_text, (0, 255, 255), 100, 200)
    render_text('', shark.name, (255, 255, 255), 600, 70)
    #updater.draw()
    all_sprites.draw(screen)
    updater.update(events=events) 
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()
