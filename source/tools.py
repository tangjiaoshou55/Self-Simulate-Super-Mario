# tools & game's master control
import pygame
import os


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.state_dict =state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                     self.keys = pygame.key.get_pressed()
                elif event.type == pygame. KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()

            pygame.display.update()
            self.clock.tick(60)

def load_graphics(path, accept=('.jpg', '.png', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
        graphics[name] = img
    return graphics

def get_image(sheet, x, y, width, height, colorkey, scale):
    if colorkey == (0, 0, 0):
        image = sheet.subsurface(pygame.Rect(x, y, width, height))
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    else:
        image = pygame.Surface((width, height))
        image.blit(sheet, (0, 0), pygame.Rect(x, y, width, height))  # (0,0) means where to draw, x,y,w,h means which part will extract form the sheet
        image.set_colorkey(colorkey)
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    return image