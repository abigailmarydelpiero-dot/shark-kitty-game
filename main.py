import sys, pygame, random, math, thorpy as tp
from state_machine.my_states import HappyState
import animation.spritesheet as spritesheet
from animation.sprite_strip_anim import SpriteStripAnim

dt = 0

class Sharkitty(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filename = "assets/images/shark1.png"
        #self.image = pygame.image.load("shark.png").convert_alpha()
        #self.rect = self.image.get_rect()
        #self.rect.topleft = (175, 175) 
        #self.rect_start_pos = self.rect.topleft
        self.name = "no name :("

        #state
        self.state = HappyState()
        #anim
        self.FPS = 120
        self.frames = self.FPS / 6
        self.strips = [
            SpriteStripAnim(self.filename, (0,0,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,32,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,64,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,96,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,128,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,160,32,32), 1, 1, True, self.frames)
        ]
        self.n = 0
        self.strips[self.n].iter()
        self.image = self.strips[self.n].next()

        #sprite box
        self.rect = self.image.get_rect()
        self.rect.topleft = (205, 175) 
        self.rect_start_pos = self.rect.topleft
    def change_animation(self, new_strip_index):
        if self.n != new_strip_index:
            self.n = new_strip_index
            self.strips[self.n].iter() #reset frame to 0
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
    def on_event(self, event):

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)
        #print(self.state)
    def update(self):
        
        state_name = str(self.state)
        
        if state_name == "HappyState":
            self.change_animation(0)
        elif state_name == "UwuState":
            self.change_animation(1)
        elif state_name == "SadState":
            self.change_animation(2)
        elif state_name == "DirtState":
            self.change_animation(3)
        elif state_name == "SickState":
            self.change_animation(4)
        elif state_name == "FoodState":
            self.change_animation(5)

        self.image = self.strips[self.n].next()

class Meat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() # Initialize the Sprite parent class
        self.image = pygame.image.load("assets/images/good_meat.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        #self.speed = 5
        self.dy = 40
        self.grv = 8
    def update(self):
        self.dy += self.grv
        self.rect.y += self.dy * dt
        if self.rect.y >= (shark.rect.topleft[1] + 20):
            self.kill()
            global happyness
            happyness += 50
            shark.on_event('fed')

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load("assets/images/pixil-frame-0(1).png").convert()
        self.offset_spd = 60
        self.mvn_offset = 0
    def moveTiles(self, dt):
        self.mvn_offset += self.offset_spd * dt
        if self.mvn_offset >= 320:
            self.mvn_offset = 0
    def tileBackground(self, screen: pygame.display) -> None:
        screenWidth, screenHeight = screen.get_size()
        imageWidth, imageHeight = self.img.get_size()
        
        # Calculate how many tiles we need to draw in x axis and y axis
        tilesX = math.ceil(screenWidth / imageWidth)
        tilesY = math.ceil(screenHeight / imageHeight)
        
        # Loop over both and blit accordingly
        for x in range(tilesX + 1):
            for y in range(tilesY):
                screen.blit(self.img, ((x * imageWidth - self.mvn_offset), y * imageHeight) )
        
pygame.init()

size = width, height = 800, 600

my_font = pygame.font.Font("/home/dalek/shark-kitty/assets/fonts/JetBrains_Mono/JetBrainsMono-VariableFont_wght.ttf", 30)

all_sprites = pygame.sprite.Group()

pygame.display.set_caption('Sharkitty')

black = '#282828'
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#pygame.event.set_grab(True)

fish_image = pygame.image.load("/home/dalek/shark-kitty/assets/images/fish.png").convert_alpha()
pygame.display.set_icon(fish_image)

def render_text(text, value, color, x, y):
    text_string = f"{text}" + f"{value}" 
    text_display = my_font.render(text_string, True, color)
    screen.blit(text_display, (x, y)) 

def feed_shark():
    shark.on_event('beingfed')
    #shark.rect.y -=200 * dt
    global gold, happyness         
    gold -= 1
    meat = Meat(random.randint(250, 300), -200)
    all_sprites.add(meat)
    

def wash_state():
    global wash_yesno
    wash_yesno = not wash_yesno

def wash_shark(event):
    global happyness
    if shark.rect.collidepoint((mx, my)):
        if event.type == pygame.MOUSEMOTION:
            motion_vector = pygame.math.Vector2(event.rel)
            #print(motion_vector.length())
            if motion_vector.length() > 20:
                happyness += 1


feed_button_xy = (700, 200)
wash_button_xy = (700, 250)

#ui - thorpy
tp.init(screen, tp.theme_classic)


feed_button = tp.Button("feed")
feed_button.center_on(feed_button_xy)
feed_button.at_unclick = feed_shark

wash_button = tp.Button("wash")
wash_button.center_on(wash_button_xy)
wash_button.at_unclick = wash_state


#mode none allows for costom positioning of buttons
my_ui_elements = tp.Group([feed_button, wash_button], mode=None)
updater = my_ui_elements.get_updater()

#beginning varibles
gold = 100
age = 0
happyness = 400
user_text = ""
wash_yesno = False


shark = Sharkitty()
all_sprites.add(shark)

tiles = Tiles()

while True:
    events = pygame.event.get()
    mx, my = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()
    #print (pygame.mouse.get_focused())
        shark.enter_name(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                #click ig
                pass
        if wash_yesno:
            wash_shark(event)

    
    if gold <= 0:
        sys.exit()
    
    
   

    if (random.randint(0,10000) == 1):
            shark.on_event('sick')
            
            #screen.blit(sick, sick_rect)
    all_sprites.update() 
    #Sharkitty.update()
    #screen.fill(black)
    #tiles
    tiles.moveTiles(dt)
    tiles.tileBackground(screen)
    

    #screen.blit(Sharkitty.image, Sharkitty.rect)
    #screen.blit(gold_text, (100, 100)) 
    #screen.blit(happyness_text, (100, 200)) 
    render_text('Gold: ', gold, (255, 255, 0), 0, 100)
    render_text('Happiness: ', happyness, (255, 255, 255), 0 , 150)
    render_text('Name Input: ', user_text, (0, 255, 255), 0, 200)
    render_text('State: ', shark.state, (0, 255, 255), 0, 250)
    render_text('', shark.name, (255, 255, 255), 600, 70)

    
    #updater.draw()
    all_sprites.draw(screen)
    updater.update(events=events) 

   

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()
