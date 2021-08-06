import pygame as pygame, sys
import wordlist

class Game:

    def __init__(self, w, h, bgc, fc, fps):
        self.pygame = pygame
        self.sys = sys
        self.fps = fps
        self.pygame.init()
        self.clock = pygame.time.Clock()
        self.width = w
        self.height = h
        self.bgColor = bgc
        self.fontColor = fc
        self.screen = self.pygame.display.set_mode((self.width, self.height))
        self.pygame.display.set_caption("VimTyper")
        self.mode = "normal"
        self.text = ""
        self.font = pygame.font.SysFont(None, 100)
        self.change = False
        self.delete = False

    def game_loop(self):
        #Game loop
        while (True):
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT: #The user closed the window!
                    self.pygame.quit()
                    self.sys.exit() #Stop running
                elif event.type == self.pygame.KEYDOWN: 
                    #If in normalmode
                    if self.mode == "normal":
                        self.normal_mode(event)
                    #If in insert mode
                    else:
                        self.insert_mode(event)


            #set frames/second
            self.draw()
            self.render_text()
            self.update()
            self.clock.tick(self.fps)

    def render_text(self):
        textSurface = self.font.render(self.text, True, self.fontColor)
        self.screen.blit(textSurface, textSurface.get_rect(center = self.screen.get_rect().center))

    def insert_mode(self, event):
        if event.key == self.pygame.K_ESCAPE:
            self.mode = "normal"
        
        elif event.key == self.pygame.K_BACKSPACE:
            self.pop_text()

        else:
            self.insert_text(event)

    def normal_mode(self, event):
        if self.change:
            self.perform_change(event)

        elif self.delete:
            self.perform_delete(event)

        else:
            if event.key == self.pygame.K_c:
                self.change = True

            if event.key == self.pygame.K_d:
                self.delete = True

            if event.key == self.pygame.K_i:
                self.mode = "insert"
    
    def perform_change(self, event):
        if event.key == self.pygame.K_c:
            self.delete_text(event)
            self.mode = "insert"
        
        if event.key == self.pygame.K_w:
            #add ability to change word
            pass
        
        self.change = False

    def perform_delete(self, event):
        if event.key == self.pygame.K_d:
            self.delete_text(event)
        
        if event.key == self.pygame.K_w:
            #add ability to del word
            pass
        
        self.delete = False

    def delete_text(self, event):
        self.text = ""

    def insert_text(self, event):
        self.text += event.unicode

    def pop_text(self):
        self.text = self.text[:-1]

    def update(self):
        self.pygame.display.update()

    def draw(self):
        self.screen.fill(self.bgColor)

bgc = (45, 45, 45)
fc = (171, 171, 171)
fps = 30
w = 600
h = 600

game = Game(w, h, bgc, fc, fps)
game.game_loop()
