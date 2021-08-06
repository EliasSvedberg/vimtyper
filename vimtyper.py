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
                        if event.key == self.pygame.K_i:
                            self.mode = "insert"

                    #If in insert mode
                    else:
                        self.insertText(event)


            #set frames/second
            self.draw()
            self.render_text()
            self.update()
            self.clock.tick(self.fps)

    def render_text(self):
        textSurface = self.font.render(self.text, True, self.fontColor)
        self.screen.blit(textSurface, textSurface.get_rect(center = self.screen.get_rect().center))

    def insertText(self, event):
        self.text += event.unicode

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
