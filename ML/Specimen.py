# STEP 2.1
import random

import numpy as np
import pygame

# Offset for calculating items relative to John Green Bot
OFFSETS = [
    pygame.Vector2(x, y) for x in [-800, 0, 800] for y in [-800, 0, 800]
]


class Specimen:
    def __init__(self, group):
        self.NINPUTS = 7
        self.NOUTPUTS = 3
        self.NHIDDEN = 1
        self.HIDDENSIZE = 15

        self.inputLayer = np.zeros((self.NINPUTS, self.HIDDENSIZE))
        self.interLayers = np.zeros((self.HIDDENSIZE, self.HIDDENSIZE, self.NHIDDEN))
        self.outputLayer = np.zeros((self.HIDDENSIZE, self.NOUTPUTS))

        self.inputBias = np.zeros((self.HIDDENSIZE))
        self.interBiases = np.zeros((self.HIDDENSIZE, self.NHIDDEN))
        self.outputBias = np.zeros((self.NOUTPUTS))

        self.inputValues = np.zeros((self.NINPUTS))
        self.outputValues = np.zeros((self.NOUTPUTS))

    def activation(self, value):
        """
        Activation function, i.e., when to shoot or move.
        """
        return 0 if value < 0 else value

    def evaluate(self):
        """
        Calculate the final output values by evaluating the parameters of the
        speciment. Pass output values through activation function.
        """
        terms = np.dot(self.inputValues, self.inputLayer) + self.inputBias
        for i in range(self.NHIDDEN):
            terms = np.array([self.activation(np.dot(terms, self.interLayers[j, :, i])) for j in
                              range(self.HIDDENSIZE)]) + self.interBiases[:, i]
        self.outputValues = np.dot(terms, self.outputLayer) + self.outputBias
        return self.outputValues

    def mutate(self):
        """
        Mutate the parameters of the specimen with a probability of 0.05 using a
        Gaussian function with standard deviation of 1. The gaussian function is
        important because it allows most mutations to be small, but a few to be
        very large.
        """
        RATE = 1.0
        PROB = 0.05

        for i in range(self.NINPUTS):
            for j in range(self.HIDDENSIZE):
                if (random.random() < PROB):
                    self.inputLayer[i, j] += random.gauss(0.0, RATE)
        for i in range(self.HIDDENSIZE):
            for j in range(self.HIDDENSIZE):
                for k in range(self.NHIDDEN):
                    if (random.random() < PROB):
                        self.interLayers[i, j, k] += random.gauss(0.0, RATE)
        for i in range(self.HIDDENSIZE):
            for j in range(self.NOUTPUTS):
                if (random.random() < PROB):
                    self.outputLayer[i, j] += random.gauss(0.0, RATE)

        for i in range(self.HIDDENSIZE):
            if (random.random() < PROB):
                self.inputBias[i] += random.gauss(0.0, RATE)
        for i in range(self.HIDDENSIZE):
            for j in range(self.NHIDDEN):
                if (random.random() < PROB):
                    self.interBiases[i, j] += random.gauss(0.0, RATE)
        for i in range(self.NOUTPUTS):
            if (random.random() < PROB):
                self.outputBias[i] += random.gauss(0.0, RATE)

