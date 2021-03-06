import pygame as pygame, sys
from staticmode import Word
import wordlist
import random
import time

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
        self.gameEnded = False
        self.help = False
        self.commandText = ""
        self.timerText = "1:00"
        self.randomWordsList = []
        self.unformattedTimer = 60
        self.randomWordsListStat = []
        self.randomWordsListStatComp = []
        self.dynamicMode = True
        self.change = False
        self.delete = False
        self.fontSize = 30
        self.midFontSize = 40
        self.bigFontSize = 50
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.bigFont = pygame.font.SysFont(None, self.bigFontSize)
        self.midFont = pygame.font.SysFont(None, self.midFontSize)
        self.wordArr = wA
        self.generate_random_sample(5)
        self.start_ticks = None
        self.comparelist = []
        self.displayScoreVar = False

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
                    elif self.mode == "insert":
                        self.insert_mode(event)
                    if self.mode == "command":
                        self.command_mode(event)

            #set frames/second
            self.draw()
            if not self.help:
                self.render_random_words()
                self.render_text()
                self.render_timer()
                if self.displayScoreVar:
                    self.display_score()
                else:
                    if self.start_ticks:
                        self.update_timer()
            else:
                self.draw()
                self.render_help()
            self.render_status_bar()
            if self.mode == "command":
                self.render_command_text()
            self.check_game_status()
            self.update()
            self.clock.tick(self.fps)

    def reset_game(self):
        self.mode = "normal"
        self.text = ""
        self.help = False
        self.timerText = "1:00"
        self.randomWordsList = []
        self.randomWordsListStat = []
        self.randomWordsListStatComp = []
        self.change = False
        self.gameEnded = False
        self.delete = False
        self.generate_random_sample(5)
        self.start_ticks = None
        self.comparelist = []
        self.displayScoreVar = False

    def generate_random_sample(self, count):
        self.randomWordsList.extend(random.sample(self.wordArr, count))
        for i in range(64):
            obj = Word(random.choice(self.wordArr), i, False)
            if obj.index == 0:
                obj.current = True
            self.randomWordsListStat.append(obj)
            self.randomWordsListStatComp.append(obj)

    def render_status_bar(self):
        statusBarSurface = self.midFont.render(self.mode.upper(), True, (0, 0, 0))
        if self.mode in ("normal", "command"):
            sbColor = self.fontColor
        else:
            sbColor = (0, 204, 204)

        self.pygame.draw.rect(self.screen, sbColor, statusBarSurface.get_rect(bottomleft = (self.width // 40 , self.height // 1.085)))
        self.screen.blit(statusBarSurface, statusBarSurface.get_rect(bottomleft = (self.width // 40 , self.height // 1.085)))

    def render_random_words(self):
        if self.dynamicMode:
            randomWordsSurface = self.font.render(" ".join(self.randomWordsList) , True, self.fontColor)
            self.screen.blit(randomWordsSurface, randomWordsSurface.get_rect(midleft = (self.width // 4 , self.height // 6)))
        else:
            # for i, line in enumerate(self.randomWordsListStat):
            #     lineText = " ".join(line)
            #     randomWordsSurface = self.font.render(lineText, True, self.fontColor)
            #     self.screen.blit(randomWordsSurface, randomWordsSurface.get_rect(midleft = (self.width // 8 , self.height // 6 + i * self.font.get_height())))
            yPos = 0
            xPos = 0
            randomWordsSurface = None
            for ind, instance in enumerate(self.randomWordsListStat):
                # fix how to display and with colors
                if (ind + 1) % 8 == 0:
                    yPos += self.font.get_height()
                    xPos = 0
                else:
                    if randomWordsSurface:
                        xPos += randomWordsSurface.get_width() + 5
                randomWordsSurface = self.font.render(instance.word, True, instance.get_color())
                self.screen.blit(randomWordsSurface, randomWordsSurface.get_rect(midleft = (self.width // 8 + xPos , self.height // 6 + yPos)))

    def submit_word(self):
        if not self.gameEnded:
            self.compare()
        self.pop_word()
        if self.dynamicMode:
            self.generate_random_sample(1)
        self.delete_text()

    def submit_command(self):
        self.perform_command()
        self.delete_command_text()

    def perform_command(self):
        if self.commandText == ":restart":
            self.reset_game()
        elif self.commandText == ":help":
            self.help = True
        elif self.commandText == ":q":
            self.mode = "normal"
            self.help = False
        elif self.commandText == ":mode static":
            self.dynamicMode = False
            self.reset_game()
        elif self.commandText == ":mode dynamic":
            self.dynamicMode = True
            self.reset_game()
        else:
            print("You entered a bad command")

    def compare(self):
        if self.dynamicMode:
            if self.text == self.randomWordsList[0]:
                self.comparelist.append(1)
            else:
                self.comparelist.append(0)
        else:
            if self.randomWordsListStatComp:
                if self.text == self.randomWordsListStatComp[0].word:
                    self.comparelist.append(1)
                    self.randomWordsListStatComp[0].visited = True
                    self.randomWordsListStatComp[0].correct = True
                else:
                    self.comparelist.append(0)
                    self.randomWordsListStatComp[0].visited = True
                    self.randomWordsListStatComp[0].correct = False

                for w in self.randomWordsListStat:
                    if w.get_index() == self.randomWordsListStatComp[0].get_index():
                        w.visited = self.randomWordsListStatComp[0].visited
                        w.correct = self.randomWordsListStatComp[0].correct
                    if len(self.randomWordsListStatComp) > 1:
                        if w.get_index() == self.randomWordsListStatComp[0].get_index() + 1:
                            w.current = True



    def check_game_status(self):
        if not self.dynamicMode:
            if not self.randomWordsListStatComp:
                self.gameEnded = True
                self.displayScoreVar = True

    def render_help(self):
        helpTextList = ["Normal mode:",
                    "<cc>: Cut text -> Insert mode",
                    "<dd>: Delete text -> normal mode",
                    "Command mode:",
                    "help: Help menu",
                    "restart: Restart game",
                    "mode: static & dynamic -> switch modes",
                    "Insert mode:",
                    "<ESC>: -> Normal mode"
                    ]
        stringVertLoc = 0
        padding = 15
        for index, line in enumerate(helpTextList):
            if line in ("Insert mode:", "Normal mode:", "Command mode:"):
                helpSurface = self.bigFont.render(line, True, self.fontColor)
                self.screen.blit(helpSurface, helpSurface.get_rect(topleft = (self.width // 4, self.height // 6 + stringVertLoc)))
                stringVertLoc += self.bigFont.get_height() + padding
            else:
                helpSurface = self.font.render(line, True, self.fontColor)
                self.screen.blit(helpSurface, helpSurface.get_rect(topleft = (self.width // 4, self.height // 6 + stringVertLoc)))
                stringVertLoc += self.font.get_height() + padding

    def render_text(self):
        textSurface = self.font.render(self.text, True, self.fontColor)
        self.screen.blit(textSurface, textSurface.get_rect(center = (self.width // 2, self.height // (3 if self.dynamicMode else 1.5))))

    def render_command_text(self):
        commandTextSurface = self.font.render(self.commandText, True, (250, 249, 246))
        self.screen.blit(commandTextSurface, commandTextSurface.get_rect(bottomleft = (self.width // 40 , self.height // 1.025)))

    def update_timer(self):
        self.unformattedTimer = 60 - (self.pygame.time.get_ticks() - self.start_ticks)// 1000

        if self.unformattedTimer == 60:
            self.timerText = "1:00"
        elif self.unformattedTimer >= 10:
            self.timerText = "0:" + str(self.unformattedTimer)
        elif self.unformattedTimer > 0:
            self.timerText = "0:0" + str(self.unformattedTimer)
        else:
            self.timerText = "0:00"
            self.displayScoreVar = True
            self.gameEnded = True

    def display_score(self):
        if self.comparelist:
            if self.dynamicMode:
                self.percentageScore = round(100 * sum(self.comparelist) / len(self.comparelist), 2)
                self.wpmScore = sum(self.comparelist)
                self.percentageScoreText = "Accuracy: " + str(self.percentageScore) + "%"
                self.wordsPerMinuteText = "WPM: " + str(self.wpmScore)
            else:
                self.percentageScore = round(100 * sum(self.comparelist) / len(self.comparelist), 2)
                self.wpmScore = round(60 * sum(self.comparelist) / (60 - self.unformattedTimer), 2)
                self.percentageScoreText = "Accuracy: " + str(self.percentageScore) + "%"
                self.wordsPerMinuteText = "WPM: " + str(self.wpmScore)

            if self.percentageScore >= 95:
                percentageColor = (126, 173, 105)
            elif self.percentageScore >= 85:
                percentageColor = (223, 192, 10)
            else:
                percentageColor = (199, 17, 80)

            if self.wpmScore >= 100:
                wpmColor = (126, 173, 105)
            elif self.wpmScore >= 75:
                wpmColor = (223, 192, 10)
            else:
                wpmColor = (199, 17, 80)

            percentageScoreSurface = self.bigFont.render(self.percentageScoreText, True, percentageColor)
            self.screen.blit(percentageScoreSurface, percentageScoreSurface.get_rect(center = (self.width // 2 , self.height // 1.8)))

            wpmSurface = self.bigFont.render(self.wordsPerMinuteText, True, wpmColor)
            self.screen.blit(wpmSurface, wpmSurface.get_rect(center = (self.width // 2 , self.height // 1.55)))

            infoSurface = self.bigFont.render("Hit ESC+Enter to Restart", True, self.fontColor)
            self.screen.blit(infoSurface, infoSurface.get_rect(center = (self.width // 2 , self.height // 1.3)))

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
            if event.key == self.pygame.K_RETURN:
                self.reset_game()
            if event.key == self.pygame.K_PERIOD:
                mods = self.pygame.key.get_mods()
                if mods & self.pygame.KMOD_SHIFT:
                    self.mode = "command"

    def command_mode(self, event):
        if event.key == self.pygame.K_ESCAPE:
            self.mode = "normal"
            self.delete_command_text()
        elif event.key == self.pygame.K_RETURN:
            self.submit_command()
        elif event.key == self.pygame.K_BACKSPACE:
            self.pop_command_text()
        else:
            self.insert_command_text(event)

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

    def delete_command_text(self):
        self.commandText = ""

    def insert_text(self, event):
        self.text += event.unicode

    def insert_command_text(self, event):
        self.commandText += event.unicode

    def pop_text(self):
        self.text = self.text[:-1]

    def pop_command_text(self):
        self.commandText = self.commandText[:-1]

    def pop_word(self):
        if self.dynamicMode:
            if self.randomWordsList:
                self.randomWordsList.pop(0)
        else:
            if self.randomWordsListStatComp:
                self.randomWordsListStatComp.pop(0)

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
