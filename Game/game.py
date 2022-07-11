import time

import pygame
from pygame import mixer

from Game.fighter import Fighter


class Game:
    def __init__(self):
        self.scaled_bg = None
        self.round_over_time = None
        mixer.init()
        pygame.init()

        # create game window
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 600

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.pygame.display.set_caption("Brawler")

        # set framerate
        self.timer = 0
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # define colours
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

        # define game variables
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # player scores. [P1, P2]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000

        # define fighter variables
        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72, 56]
        self.WARRIOR_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET]
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [112, 107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET]

        # load music and sounds
        pygame.mixer.music.load("../assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.sword_fx = pygame.mixer.Sound("../assets/audio/sword.wav")
        self.sword_fx.set_volume(0.5)
        self.magic_fx = pygame.mixer.Sound("../assets/audio/magic.wav")
        self.magic_fx.set_volume(0.75)

        # load background image
        self.bg_image = pygame.image.load("../assets/images/background/background.jpg").convert_alpha()

        # load spritesheets
        self.warrior_sheet = pygame.image.load("../assets/images/warrior/Sprites/warrior.png").convert_alpha()
        self.wizard_sheet = pygame.image.load("../assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # load vicory image
        self.victory_img = pygame.image.load("../assets/images/icons/victory.png").convert_alpha()

        # define number of steps in each animation
        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        # define font
        self.count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
        self.score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

        self.fighter_1 = Fighter(1, 200, 310, False, self.WARRIOR_DATA, self.warrior_sheet,
                                 self.WARRIOR_ANIMATION_STEPS,
                                 self.sword_fx)
        self.fighter_2 = Fighter(2, 700, 310, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS,
                                 self.magic_fx)

    # function for drawing text
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    # function for drawing background
    def draw_bg(self):
        self.scaled_bg = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(self.scaled_bg, (0, 0))

    # function for drawing fighter health bars
    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, 400 * ratio, 30))

    # create two instances of fighters

    # game loop
    def runGame(self, AI):
        run = True
        start = time.time()

        while run:
            curTime = time.time()
            if curTime - start >= 20:
                self.timer = curTime - start
                run = False
            self.clock.tick(self.FPS)

            # draw background
            self.draw_bg()

            # show player stats
            self.draw_health_bar(self.fighter_1.health, 20, 20)
            self.draw_health_bar(self.fighter_2.health, 580, 20)
            self.draw_text("P1: " + str(self.score[0]), self.score_font, self.RED, 20, 60)
            self.draw_text("P2: " + str(self.score[1]), self.score_font, self.RED, 580, 60)

            data = AI.apply_input(self)
            # update countdown
            if self.intro_count <= 0:
                # move fighters
                self.fighter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_2,
                                    self.round_over, data[0])
                self.fighter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, self.fighter_1,
                                    self.round_over, data[1])
            else:
                # display count timer
                self.draw_text(str(self.intro_count), self.count_font, self.RED, self.SCREEN_WIDTH / 2,
                               self.SCREEN_HEIGHT / 3)
                # update count timer
                if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()

            # update fighters
            self.fighter_1.update()
            self.fighter_2.update()

            # draw fighters
            self.fighter_1.draw(self.screen)
            self.fighter_2.draw(self.screen)

            # check for player defeat
            if not self.round_over:
                if not self.fighter_1.alive:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif not self.fighter_2.alive:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                # display victory image
                self.screen.blit(self.victory_img, (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    run = False
                    self.intro_count = 3
                    self.fighter_1 = Fighter(1, 200, 310, False, self.WARRIOR_DATA, self.warrior_sheet,
                                             self.WARRIOR_ANIMATION_STEPS,
                                             self.sword_fx)
                    self.fighter_2 = Fighter(2, 700, 310, True, self.WIZARD_DATA, self.wizard_sheet,
                                             self.WIZARD_ANIMATION_STEPS, self.magic_fx)

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # update display
            pygame.display.update()

        end = time.time()
        fitnessScore = ((end - start) * -0.3) + self.fighter_1.jumps + self.fighter_2.jumps + (
                100 - self.fighter_1.health) + (
                               100 - self.fighter_2.health)
        return fitnessScore
    # runGame()
