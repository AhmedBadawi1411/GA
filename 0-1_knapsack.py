import random

ITEMS = [
    {"name": "A", "weight": 12, "value": 4},
    {"name": "B", "weight": 2,  "value": 2},
    {"name": "C", "weight": 1,  "value": 2},
    {"name": "D", "weight": 1,  "value": 1},
    {"name": "E", "weight": 4,  "value": 10},
    {"name": "F", "weight": 3,  "value": 5},
    {"name": "G", "weight": 5,  "value": 8},
    {"name": "H", "weight": 2,  "value": 4},
    {"name": "I", "weight": 6,  "value": 9},
    {"name": "J", "weight": 4,  "value": 7},
    {"name": "K", "weight": 7,  "value": 11},
    {"name": "L", "weight": 3,  "value": 6},
    {"name": "M", "weight": 8,  "value": 12},
    {"name": "N", "weight": 1,  "value": 3},
    {"name": "O", "weight": 5,  "value": 7},
    {"name": "P", "weight": 9,  "value": 13},
    {"name": "Q", "weight": 2,  "value": 5},
    {"name": "R", "weight": 6,  "value": 10},
    {"name": "S", "weight": 4,  "value": 6},
    {"name": "T", "weight": 3,  "value": 4},
    {"name": "U", "weight": 7,  "value": 9},
    {"name": "V", "weight": 2,  "value": 3},
    {"name": "W", "weight": 5,  "value": 8},
    {"name": "X", "weight": 8,  "value": 14},
    {"name": "Y", "weight": 1,  "value": 2},
    {"name": "Z", "weight": 6,  "value": 11},
    {"name": "AA", "weight": 3, "value": 5},
    {"name": "AB", "weight": 4, "value": 8},
    {"name": "AC", "weight": 7, "value": 12},
    {"name": "AD", "weight": 2, "value": 4},
    {"name": "AE", "weight": 9, "value": 15},
    {"name": "AF", "weight": 5, "value": 9},
    {"name": "AG", "weight": 1, "value": 1},
    {"name": "AH", "weight": 6, "value": 8},
    {"name": "AI", "weight": 4, "value": 7},
    {"name": "AJ", "weight": 8, "value": 13},
    {"name": "AK", "weight": 3, "value": 6},
    {"name": "AL", "weight": 7, "value": 10},
    {"name": "AM", "weight": 2, "value": 3},
    {"name": "AN", "weight": 5, "value": 10},
    {"name": "AO", "weight": 9, "value": 12},
    {"name": "AP", "weight": 1, "value": 4},
    {"name": "AQ", "weight": 6, "value": 9},
    {"name": "AR", "weight": 4, "value": 5},
    {"name": "AS", "weight": 8, "value": 15},
    {"name": "AT", "weight": 3, "value": 7},
    {"name": "AU", "weight": 5, "value": 6},
    {"name": "AV", "weight": 2, "value": 2},
    {"name": "AW", "weight": 7, "value": 13},
    {"name": "AX", "weight": 4, "value": 9},
]

MAX_CAPACITY = 100
POP_SIZE = 8
GENERATIONS = 30
MUTATION_RATE = 0.05
ELITE_COUNT = 1
TRIES = 10
IMPROVEMENT_TOLERANCE = 0.01

def create_chromosome():
      return [random.randint(0,1) for _ in range(len(ITEMS))]

def calculate_fitness(chromosome):
      total_wieght = sum(gene * item['weight'] for gene, item in zip(chromosome, ITEMS))
      total_value = sum(gene * item['value'] for gene, item in zip(chromosome, ITEMS))
      
      if total_wieght > MAX_CAPACITY:
            return 0
      
      return total_value

def select_parent(population, fitnesses):
      total_fitness = sum(fitnesses)
      pick = random.uniform(0, total_fitness)
      current_fit= 0
      
      for c, f in zip(population, fitnesses):
            current_fit += f
            if current_fit >= pick:
                  return c
      
      return population[-1]

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]  
    return chromosome


def terminator(best_fit, prev_fit, tries, tolerance):
    if abs(mean_fit - prev_fit) < tolerance :
        tries -= 1
    else:
        tries = TRIES

    return tries == 0, tries
      
population = [create_chromosome() for _ in range(POP_SIZE)]

prev_fit = 0

for gen in range(1, GENERATIONS + 1):
    fitnesses = [calculate_fitness(chrom) for chrom in population]
    
    best_fit = max(fitnesses)
    mean_fit = sum(fitnesses) / len(fitnesses)
    best_chrom = population[fitnesses.index(best_fit)]
    print(f"Generation {gen:02d} | Best Chromosome: {best_chrom} | Best Fitness: {best_fit} | Mean Fitness: {mean_fit}")
    
    should_stop, TRIES = terminator(mean_fit, prev_fit, TRIES, IMPROVEMENT_TOLERANCE)
    
    if should_stop:
            break
    prev_fit = mean_fit
    
    new_population = [best_chrom.copy()]
    while len(new_population) < POP_SIZE:
        p1 = select_parent(population, fitnesses)
        p2 = select_parent(population, fitnesses)
        c1, c2 = crossover(p1, p2)
        new_population.append(mutate(c1))
        if len(new_population) < POP_SIZE:
            new_population.append(mutate(c2))
            
    population = new_population
    
      #? AMAZING TOPIC: Dead Initial Population 