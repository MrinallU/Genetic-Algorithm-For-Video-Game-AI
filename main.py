import multiprocessing
import Specimen


def get_fitness(group):
    """
  Fitness function used in training.
  """
    return group.calc_fitness()


# Let's say that our population size is 200. That means there are 200 different
# specimen that are competing to be in the top half.
gen_size = 200

# We're going to be doing lots of things at the same time. So we're going to
# 10 threads in the Colab system to compute things simultaneously.
nThreads = 10

# Start up a bunch of processing threads to do lots of work at the same time.
pool = multiprocessing.Pool(nThreads)

# Create gen_size number of NEW  specimen
generation = [Specimen() for i in range(gen_size)]

# The map function applies each specimen in the generation to the git_fitness
# function. Simply put, this next line of code plays 200 games at the same time,
# and collects their scores.
scores = pool.map(get_fitness, generation)

# Create a map of a specimen to its score.
specimen_score_map = {}
for i in range(len(generation)):
    specimen_score_map[generation[i]] = scores[i]

# Sort the specimen by their score and keep only the top half.
half_size = gen_size // 2
generation = sorted(specimen_score_map, key=lambda k: specimen_score_map[k], reverse=True)[0:half_size - 1]

# Initialize an interation variable because the next few cells may be run many times.
iteration = 0
