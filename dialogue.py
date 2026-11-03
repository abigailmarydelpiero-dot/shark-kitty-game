import pygame

class DialogueBox(pygame.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        # Create the surface for the box
        self.text = text
        self.size = self.width, self.height = 800,100
        self.image = pygame.Surface(self.size)
        self.color = (50,50,50)
        self.image.fill(self.color) # Dark gray background
        self.my_font = pygame.font.Font("assets/fonts/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 30)
    
        self.render_text(self.text)     
        # Position the box
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def render_text(self, text): 
        self.image.fill(self.color)
        text_display = self.my_font.render(text, True, (255,255,255))
        self.image.blit(text_display, (10,10))

#properties
#dialogue_box_width = 400
#dialogue_box_height = 200
#screen_width = main.config.get_var("width")
#screen_height = main.config.get_var("height")
#dialogue_box_x = (screen_width - dialogue_box_width)//2
#dialogue_box_y = (screen_height - dialogue_box_height)//2
#dialouge_box = False