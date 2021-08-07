import pygame as pygame, sys
import wordlist
import random

class Game:

    def __init__(self, w, h, bgc, fc, fps, wA):
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
        self.timerText = "1:00"
        self.randomWordsList = []
        self.change = False
        self.delete = False
        self.fontSize = 30
        self.bigFontSize = 50
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.bigFont = pygame.font.SysFont(None, self.bigFontSize)
        self.wordArr = wA
        self.generate_random_sample(5)
        self.start_ticks = None
        self.comparelist = []

    def game_loop(self):
        #Game loop
        while (True):
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT: #The user closed the window!
                    self.pygame.quit()
                    self.sys.exit() #Stop running
                
                elif event.type == self.pygame.KEYDOWN: 
                    #Start timer
                    if not self.start_ticks:
                        self.start_ticks = self.pygame.time.get_ticks()
                    #If in normalmode
                    if self.mode == "normal":
                        self.normal_mode(event)
                    #If in insert mode
                    else:
                        self.insert_mode(event)


            #set frames/second
            self.draw()
            self.render_random_words()
            self.render_text()
            if self.start_ticks:
                self.render_timer()
                self.update_timer()
            self.update()
            self.clock.tick(self.fps)

    def generate_random_sample(self, count):
        self.randomWordsList.extend(random.sample(self.wordArr, count)) 
        
    def render_random_words(self):
        randomWordsSurface = self.font.render(" ".join(self.randomWordsList) , True, self.fontColor)
        self.screen.blit(randomWordsSurface, randomWordsSurface.get_rect(midleft = (self.width // 4 , self.height // 6)))

    def submit_word(self):
        self.compare()
        self.pop_word()
        self.generate_random_sample(1)
        self.delete_text()

    def compare(self):
        if self.text == self.randomWordsList[0]:
            self.comparelist.append(1)
        else:
            self.comparelist.append(0)

    def render_text(self):
        textSurface = self.font.render(self.text, True, self.fontColor)
        self.screen.blit(textSurface, textSurface.get_rect(center = self.screen.get_rect().center))

    def update_timer(self):
        self.unformattedTimer = 60 - (self.pygame.time.get_ticks() - self.start_ticks)// 1000

        if self.unformattedTimer >= 10:
            self.timerText = "0:" + str(self.unformattedTimer)
        
        elif self.unformattedTimer > 0:
            self.timerText = "0:0" + str(self.unformattedTimer)
        else:
            self.timerText = "1:00"
        #fix timer updating

    def render_timer(self):
        timeSurface = self.bigFont.render(self.timerText , True, self.fontColor)
        self.screen.blit(timeSurface, timeSurface.get_rect(center = (self.width // 2 , self.height // 10)))

    def insert_mode(self, event):
        if event.key == self.pygame.K_ESCAPE:
            self.mode = "normal"
        
        elif event.key == self.pygame.K_BACKSPACE:
            self.pop_text()

        elif event.key == self.pygame.K_SPACE:
            self.submit_word()
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
            self.delete_text()
            self.mode = "insert"
        
        if event.key == self.pygame.K_w:
            #add ability to change word
            pass
        
        self.change = False

    def perform_delete(self, event):
        if event.key == self.pygame.K_d:
            self.delete_text()
        
        if event.key == self.pygame.K_w:
            #add ability to del word
            pass
        
        self.delete = False

    def delete_text(self):
        self.text = ""

    def insert_text(self, event):
        self.text += event.unicode

    def pop_text(self):
        self.text = self.text[:-1]

    def pop_word(self):
        if self.randomWordsList:
            self.randomWordsList.pop(0)

    def update(self):
        self.pygame.display.update()

    def draw(self):
        self.screen.fill(self.bgColor)

bgc = (45, 45, 45)
fc = (171, 171, 171)
fps = 30
w = 600
h = 600
wA = wordlist.wordArr

game = Game(w, h, bgc, fc, fps, wA)
game.game_loop()
