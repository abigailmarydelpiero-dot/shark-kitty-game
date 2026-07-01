import pygame
import animation.spritesheet as spritesheet

class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, rect, count, colorkey=None, loop=False, frames=2):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = spritesheet.spritesheet(filename)
        # Load the base 32x32 frames
        base_images = ss.load_strip(rect, count, colorkey)
        
        # FIX: Scale each frame up (e.g., scale_factor=4 turns 32x32 into 128x128)
        self.images = []
        for img in base_images:
            w, h = img.get_size()
            scaled_img = pygame.transform.scale(img, (w * 10, h * 10))
            self.images.append(scaled_img)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames
    def iter(self):
        self.i = 0
        self.f = self.frames
        return self
    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                self.i = len(self.images) - 1
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self