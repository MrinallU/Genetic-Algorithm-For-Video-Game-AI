# STEP 2.1
import numpy as np
import pygame

import game
from Specimen import Specimen

# Offset for calculating items relative to John Green Bot
OFFSETS = [
    pygame.Vector2(x, y) for x in [-800, 0, 800] for y in [-800, 0, 800]
]


class Group:
    def __init__(self):
        """
        Create a specimen (i.e., one of John Green Bot's brains)

        25 inputs: 5 attributes (x, y, x_vel, y_vel, radius) of nearest trash
        objects

        5 outputs: 5 moves (x, y, aim_x, aim_y, blast)
        """
        # self.NINPUTS = 25
        # self.NOUTPUTS = 5
        # self.NHIDDEN = 1
        # self.HIDDENSIZE = 15

        self.s1 = Specimen(self)
        self.s2 = Specimen(self)

        self.NINPUTS = 25
        self.NOUTPUTS = 5
        self.NHIDDEN = 1
        self.HIDDENSIZE = 15

        self.inputLayer = np.zeros((self.NINPUTS, self.HIDDENSIZE))
        self.interLayers = np.zeros((self.HIDDENSIZE, self.HIDDENSIZE, self.NHIDDEN))
        self.outputLayer = np.zeros((self.HIDDENSIZE, self.NOUTPUTS))

        self.inputBias = np.zeros((self.HIDDENSIZE))
        self.interBiases = np.zeros((self.HIDDENSIZE, self.NHIDDEN))
        self.outputBias = np.zeros((self.NOUTPUTS))

        self.inputValues = np.zeros((self.NINPUTS))
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
        game.runGame()
        return game.run(AI=self)

    def min_offset(self, point1, point2):
        """
        Helper function for apply_input
        """
        candidates = (point2 - point1 + v for v in OFFSETS)
        return min(candidates, key=lambda v: v.length_squared())

    def apply_input(self, game):
        """
        This function takes the game state, loads it into the neural network,
        computes the output, and performs the output actions.
        """
        # john_green_bot = game.john_green_bot
        #
        # offsets = {a: self.min_offset(john_green_bot.position, a.position) for a in game.trash_list}
        #
        # trash_list = sorted(game.trash_list, key=lambda a: offsets[a].length_squared())
        # visible_trash = []
        # if len(trash_list) > 5: visible_trash = trash_list[0:4]
        #
        # # Get all the trash and add them as inputs to the neural network
        # for i in range(len(visible_trash)):
        #     self.inputValues[5 * i + 0] = offsets[visible_trash[i]].x
        #     self.inputValues[5 * i + 1] = offsets[visible_trash[i]].y
        #     self.inputValues[5 * i + 2] = visible_trash[i].moveDirection.x if abs(
        #         visible_trash[i].moveDirection.x) > 0.5 else 0
        #     self.inputValues[5 * i + 3] = visible_trash[i].moveDirection.y if abs(
        #         visible_trash[i].moveDirection.y) > 0.5 else 0
        #     self.inputValues[5 * i + 4] = visible_trash[i].radius
        #
        # for i in range(len(visible_trash) * 5, 5 * 5):
        #     self.inputValues[i] = 0.0

        # Set the input values for each player's nueral network using the other player's data.


        # Compute the output
        outputValues = self.evaluate()
        outputValuesP1 = outputValues[0]
        outputValuesP2 = outputValues[1]

        # Actually do the recommended actions (apply the actions to each player in the game, use the player)