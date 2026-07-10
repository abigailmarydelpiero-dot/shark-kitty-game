import sys, pygame, random, math, thorpy as tp
from state_machine.my_states import SadState
import animation.spritesheet as spritesheet
from animation.sprite_strip_anim import SpriteStripAnim

dt = 0

class Sharkitty(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filename = "assets/images/shark1.png"
        self.name = "no name :["

        #state
        self.state = SadState()
        #anim
        self.FPS = 120
        self.frames = self.FPS / 6
        self.strips = [
            SpriteStripAnim(self.filename, (0,0,32,32), 2, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,32,32,32), 2, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,64,32,32), 2, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,96,32,32), 2, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,128,32,32), 2, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,160,32,32), 1, 1, True, self.frames),
            SpriteStripAnim(self.filename, (0,192,32,32), 2, 1, True, self.frames)
        ]
        self.n = 0
        self.strips[self.n].iter()
        self.image = self.strips[self.n].next()

        #sprite box
        self.rect = self.image.get_rect()
        self.rect.topleft = (350, 175) 
        self.rect_start_pos = self.rect.topleft
    def change_animation(self, new_strip_index):
        if self.n != new_strip_index:
            self.n = new_strip_index
            self.strips[self.n].iter() #reset frame to 0
    def enter_name(self, event):
        global user_text, entering_name
        
        if entering_name:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    print(f"Submitted Text: {user_text}")
                    self.name = user_text
                    user_text = ""
                    entering_name = False
                    top_panel.set_title(str(shark.name))
                    
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
        elif state_name == "WorkState":
            self.change_animation(6)

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
        self.img = pygame.image.load("assets/images/pixil-frame-0(2).png").convert()
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

my_font = pygame.font.Font("assets/fonts/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 30)

all_sprites = pygame.sprite.Group()

pygame.display.set_caption('Sharkitty')

black = '#282828'
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#pygame.event.set_grab(True)



pointer_img = pygame.image.load("assets/images/pixilart-frames/hand2.png").convert_alpha()
hand_img = pygame.image.load("assets/images/pixilart-frames/hand1.png").convert_alpha()
sponge_img = pygame.image.load("assets/images/pixilart-frames/sponge.png").convert_alpha()
hotspot = (20, 10)
pointer_cursor = pygame.cursors.Cursor(hotspot, pointer_img)
hand_cursor = pygame.cursors.Cursor(hotspot, hand_img)
sponge_cursor = pygame.cursors.Cursor(hotspot, sponge_img)

pygame.mouse.set_cursor(pointer_cursor)

fish_image = pygame.image.load("/home/dalek/shark-kitty/assets/images/fish.png").convert_alpha()
pygame.display.set_icon(fish_image)

def render_text(text, value, color, x, y):
    text_string = f"{text}" + f"{value}" 
    text_display = my_font.render(text_string, True, color)
    screen.blit(text_display, (x, y)) 

def feed_shark():
    global gold        
    gold -= 1
    print(shark.state)
    if str(shark.state) != "SickState":
        shark.on_event('beingfed')
        meat = Meat(random.randint(400, 440), -200)
        all_sprites.add(meat)
    
def cure_shark():
    shark.on_event('cured')
    global gold, happyness
    gold -= 10
    happyness += 10

def work_shark():
    shark.on_event('work')

def wash_state():
    global wash_yesno
    wash_yesno = not wash_yesno

def name_enter():
    global entering_name
    entering_name = not entering_name

def wash_shark(event):
    global happyness, dirt
    if str(shark.state) == "DirtState":
        if shark.rect.collidepoint((mx, my)):
            if event.type == pygame.MOUSEMOTION:
                motion_vector = pygame.math.Vector2(event.rel)
                #print(motion_vector.length())
                if motion_vector.length() > 20:
                    happyness += 1
                    dirt -= 1
        if dirt <= 0:
            shark.on_event('clean')
            dirt = 0

def switch_theme():
    global dtheme, now_color, wcolor, dcolor
    dtheme = not dtheme
    

def get_all_elements(element):
    #flattens a UI element ree into a single list
    
    elements = [element]

    #check if children
    if hasattr(element, "get_children"):
        for child in element.get_children():
            elements.extend(get_all_elements(child))
    return elements

right_menu_xy = (200, 350)
top_menu_xy = (200, 100)

tp.set_default_font("assets/fonts/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 30)

#beginning varibles
gold = 100
age = 0
happyness = 1000
user_text = ""
wash_yesno = False
entering_name = False
dtheme = False
sad_timer = 75
happy_timer = 75
check_timer = 75

shark = Sharkitty()

#ui - thorpy
tp.init(screen, tp.theme_text_dark)

#set elements radius to 40% of their own height, except for boxes
tp.set_style_attr("radius", 0.4, exceptions_cls=[tp.Box])


box_color = (40, 40, 40)
text_color = (213, 247, 247)


tp.set_style_attr("bck_color", (box_color, "h"), None, exceptions_cls=[ tp.Text])
tp.set_style_attr("font_color", text_color)

feed_button = tp.Button("feed")
feed_button.at_unclick = feed_shark

work_button = tp.Button("work")
work_button.at_unclick = work_shark

cure_button = tp.Button("cure")
cure_button.at_unclick = cure_shark

wash_text = tp.Text("wash")
wash_button = tp.SwitchButton(False, "auto", (20,35))
wash_button.set_style_attr("bck_color", (50, 60, 60)) 
wash_button.set_style_attr("radius", wash_button.rect.h//100)
wash_button.set_size((50, 20))
wash_button.at_unclick = wash_state
wash_full = tp.Box([wash_text, wash_button])
wash_full.sort_children("h",margins=(10, 10))

name_button = tp.Button("name")
name_button.at_unclick = name_enter

dark_mode_btn = tp.SwitchButton(False, "auto", (20, 40))
dark_mode_btn.set_style_attr("bck_color", (50, 60, 60)) 
dark_mode_btn.set_style_attr("radius", dark_mode_btn.rect.h//100)
dark_mode_btn.set_size((50, 20))
dark_mode_btn.at_unclick = switch_theme

gold_text = tp.Text(f"gold {str(gold)}")
happyness_text = tp.Text(f"happy {str(happyness)}")
state_text = tp.Text(str(shark.state).replace("State", ""))

right_panel = tp.Box([feed_button,wash_full,work_button,cure_button,name_button])
right_panel.center_on(right_menu_xy)
right_panel.set_style_attr("radius", right_panel.rect.h//100)
right_panel.sort_children(margins=(20, 30))

top_panel = tp.TitleBox(str(shark.name), children=[gold_text, happyness_text, state_text, dark_mode_btn])
top_panel.center_on(top_menu_xy)
top_panel.set_style_attr("radius", right_panel.rect.h//100)
top_panel.sort_children("h",margins=(50, 50))
#mode none allows for costom positioning of buttons
my_ui_elements = tp.Group([right_panel, top_panel], mode=None)
updater = my_ui_elements.get_updater()





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

    if dtheme:
        tiles.img = pygame.image.load("assets/images/darkbg.png").convert()
    else:
        tiles.img = pygame.image.load("assets/images/pixil-frame-0(2).png").convert()

    hovering_ui = False 

    if gold <= 0 or happyness <= 0:
        sys.exit()
    

    if str(shark.state) == "SickState":
        sad_timer -= 10
        if sad_timer <= 0:
            happyness -= 1
            sad_timer = 75
    elif str(shark.state) == "SadState":
        
        sad_timer -= 1
        if sad_timer <= 0:
            happyness -= 1
            sad_timer = 75
    elif str(shark.state) == "HappyState":
        happy_timer -= 1
        if happy_timer <= 0:
            happyness += 1
            happy_timer = 75
    elif str(shark.state) == "WorkState":
        check_timer -= 1
        if check_timer <= 0:
            happyness -= 10
            gold += 15
            check_timer = 75

    gold_text.set_text(f"gold: {str(gold)}")
    happyness_text.set_text(f"happy: {str(happyness)}")
    state_text.set_text(str(shark.state).replace("State", ""))
    
    top_panel.sort_children("h",margins=(50, 50))

    if (random.randint(0,1000) == 1):
        shark.on_event('sick')
    elif (random.randint(0,1000) == 1):
        shark.on_event('dirty')
        dirt = 50

    if (happyness <= 400):
        shark.on_event('sad')
        sad_timer = 100

            

    all_sprites.update() 

    tiles.moveTiles(dt)
    tiles.tileBackground(screen)
    

    #screen.blit(Sharkitty.image, Sharkitty.rect)
    #screen.blit(gold_text, (100, 100)) 
    #screen.blit(happyness_text, (100, 200)) 
    #render_text('Gold: ', gold, (255, 255, 0), 0, 100)
    #render_text('Happiness: ', happyness, (255, 255, 255), 0 , 150)
    render_text('Name Input: ', user_text, (0, 255, 255), 20, 500)

    #render_text('State: ', shark.state, (0, 255, 255), 0, 250)
    #render_text('', shark.name, (255, 255, 255), 600, 70)


    


    #updater.draw()
    all_sprites.draw(screen)
    updater.update(events=events) 

    all_interactive_elements = get_all_elements(right_panel) + get_all_elements(top_panel)

    for element in all_interactive_elements:
        # Verify the item has a valid coordinate boundary box
        if hasattr(element, "rect") and element.rect is not None:
            
            # Check if the mouse is physically colliding with the button/slider
            if element.rect.collidepoint((mx,my)):
                hovering_ui = True
                break

    if hovering_ui and not wash_yesno:
        pygame.mouse.set_cursor(hand_cursor)
    elif wash_yesno:
        pygame.mouse.set_cursor(sponge_cursor)
    else:
        pygame.mouse.set_cursor(pointer_cursor)



    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
