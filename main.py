import multiprocessing
import time

from ML.Group import Group


def get_fitness(group):
    """
  Fitness function used in training.
  """
    return group.calc_fitness()

# Let's say that our population size is 200. That means there are 200 different
# specimen that are competing to be in the top half.
gen_size = 10

# We're going to be doing lots of things at the same time. So we're going to
# 10 threads in the Colab system to compute things simultaneously.
# nThreads = 10

# Start up a bunch of processing threads to do lots of work at the same time.
# pool = multiprocessing.Pool(nThreads)

# Create gen_size number of NEW  specimen
generation = [Group() for i in range(gen_size)]

# The map function applies each specimen in the generation to the git_fitness
# function. Simply put, this next line of code plays 200 games at the same time,
# and collects their scores.
scores = []
for g in generation:
    f = g.calc_fitness()
    scores.append(f)

# Create a map of a specimen to its score.
specimen_score_map = {}
for i in range(len(generation)):
    specimen_score_map[generation[i]] = scores[i]

# Sort the specimen by their score and keep only the top half.
half_size = gen_size // 2
generation = sorted(specimen_score_map, key=lambda k: specimen_score_map[k], reverse=True)[0:half_size - 1]

# Initialize an interation variable because the next few cells may be run many times.
iteration = 0

# CHANGEME: How many training iterations should we do on each click?
for _ in range(10):

    # List of game states (images) that we will turn into an animation later.
    images = []

    # Increment the iteration counter
    iteration += 1

    # For each reproducer, create a copy, mutate it, and add it to the generation
    for i in range(gen_size // 2):
        child = generation[i]
        child.mutate()
        generation.append(child)

    # At this point we have a new generation. Half of these are parents/reproducers
    # and half are mutant-children.

    # The pool.map function calls the get_fitness function defined in STEP 3.1
    # "simultaneously" for each specimen in the generation
    scores = []
    for g in generation:
        f = g.calc_fitness()
        scores.append(f)

    # Create a map of specimen to its score
    specimen_score_map = {}
    for i in range(len(generation)):
        specimen_score_map[generation[i]] = scores[i]

        # Find the mean-average of the scores of all specimen
    average_of_all = sum(specimen_score_map.values()) / gen_size

    # Sort the specimen by their score and keep only the top half.
    generation = sorted(specimen_score_map, key=lambda k: specimen_score_map[k], reverse=True)[0:half_size - 1]

    # Find the top example. Call the calc_fitness function with doRender = True so
    # that it fills in the images variable with image-captures of the game play
    example_score = generation[0].calc_fitness()

    # Find the mean-average of the scores of all reproducers (i.e., the top half of
    # all specimen)
    average_of_reproducers = sum(sorted(specimen_score_map.values(), reverse=True)[0:half_size]) / half_size

    # Print the statistics
    print('ITERATION {}'.format(iteration))
    print('\tAverage score of all specimen: {:5.3f}'.format(average_of_all))
    print('\tAverage score of reproducers:  {:5.3f}'.format(average_of_reproducers))
    print('\tScore of the video-specimen:   {:5.3f}'.format(example_score))