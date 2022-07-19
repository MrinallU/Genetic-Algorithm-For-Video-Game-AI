# STEP 2.1
import numpy as np
import pygame

from Game.game import Game
from ML.Specimen import Specimen

# Offset for calculating items relative to John Green Bot
OFFSETS = [
    pygame.Vector2(x, y) for x in [-800, 0, 800] for y in [-800, 0, 800]
]


class Group:
    def __init__(self):
        """
        Create a Group of Players

        8 inputs: 8 attributes  (x, y, xVel, yVel, jumping attacking, health, time) of the other player
        5 outputs: 5 moves (x, jump, a1)
        """
        self.game = Game()
        self.s1 = Specimen(self)
        self.s2 = Specimen(self)

        self.NINPUTS = 7
        self.NOUTPUTS = 3

        self.inputValuesP2 = np.zeros((self.NINPUTS))
        self.inputValuesP1 = np.zeros((self.NINPUTS))
        self.outputValuesP1 = np.zeros((self.NOUTPUTS))
        self.outputValuesP2 = np.zeros((self.NOUTPUTS))

    def evaluate(self):
        """
        Calculate the final output values by evaluating the parameters of the
        speciment. Pass output values through activation function.
        """

        out1 = self.s1.evaluate()
        out2 = self.s2.evaluate()
        return [out1, out2]

    def mutate(self):
        """
        Mutate the parameters of the specimen with a probability of 0.05 using a
        Gaussian function with standard deviation of 1. The gaussian function is
        important because it allows most mutations to be small, but a few to be
        very large.
        """
        self.s1.mutate()
        self.s2.mutate()

    def calc_fitness(self):
        """
        This function calculates the fitness (i.e., the smartness) of the specimen
        by playing the game and returning the final score.
        """
        return self.game.runGame(AI=self)

    def min_offset(self, point1, point2):
        """
        Helper function for apply_input
        """
        candidates = (point2 - point1 + v for v in OFFSETS)
        return min(candidates, key=lambda v: v.length_squared())

    def apply_input(self):
        self.inputValuesP1[0] = self.game.fighter_2.rect.centerx
        self.inputValuesP1[1] = self.game.fighter_2.rect.centery
        self.inputValuesP1[2] = self.game.fighter_2.vel_x
        self.inputValuesP1[2] = self.game.fighter_2.vel_y
        self.inputValuesP1[4] = self.game.fighter_2.jump
        self.inputValuesP1[5] = self.game.fighter_2.attack_type if self.game.fighter_2.attacking else 0
        self.inputValuesP1[6] = self.game.fighter_2.health
        self.inputValuesP1[6] = self.game.timer

        self.inputValuesP2[0] = self.game.fighter_1.rect.centerx
        self.inputValuesP2[1] = self.game.fighter_1.rect.centery
        self.inputValuesP2[2] = self.game.fighter_1.vel_x
        self.inputValuesP2[2] = self.game.fighter_1.vel_y
        self.inputValuesP2[4] = self.game.fighter_1.jump
        self.inputValuesP2[5] = self.game.fighter_1.attack_type if self.game.fighter_2.attacking else 0
        self.inputValuesP2[6] = self.game.fighter_1.health
        self.inputValuesP2[6] = self.game.timer

        # Actually do the recommended actions (apply the actions to each player in the game, use the player)
        self.s1.inputValues = self.inputValuesP1
        self.s2.inputValues = self.inputValuesP2
        # Compute the output
        return self.evaluate()
