import random


def load_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        problem_size, capacity = map(int, lines[0].split())
        items = []
        for line in lines[1:]:
            value, weight = map(int, line.split())
            items.append((value, weight))

    return items, capacity


class KnapsackAlgorithm:
    def __init__(self, items, capacity, population_size=100, generations=500, crossover_rate=0.8, mutation_rate=0.1):
        self.items = items
        self.capacity = capacity
        self.pop_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutations_rate = mutation_rate
        self.population = self.init_population()

    def init_population(self):
        population = []
        for i in range(self.pop_size):
            chromosome = [random.randint(0, 1) for i in range(len(self.items))]
            population.append(chromosome)
        return population

    def fitness(self, chromosome):
        total_value, total_weight = 0, 0
        for i, gene in enumerate(chromosome):
            if gene == 1:
                total_value += self.items[i][0]
                total_weight += self.items[i][1]
        if total_weight > self.capacity:
            return 0
        return total_value

    def selection(self):
        fitnesses = [self.fitness(individual) for individual in self.population]
        total_fitnesses = sum(fitnesses)
        selection_probs = [f / total_fitnesses for f in fitnesses]
        selected = random.choices(self.population, weights=selection_probs, k=2)
        return selected

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return child1, child2
        return parent1, parent2

    def mutate(self, chromosome):
        for i in range(len(chromosome)):
            if random.random() < self.mutations_rate:
                chromosome[i] = 1 - chromosome[i]
        return chromosome

    def evolve(self):
        for generation in range(self.generations):
            new_population = []
            for i in range(self.pop_size // 2):
                parent1, parent2 = self.selection()
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                new_population.append(self.mutate(child2))
            self.population = new_population

            best_individual = max(self.population, key=lambda chromo: self.fitness(chromo))
            best_fitness = self.fitness(best_individual)
            print(f'Pokolenie {generation} prezentuje najlepszą wartość: {best_fitness}')

        return max(self.population, key=lambda chromo: self.fitness(chromo))


items, capacity = load_data(r"C:\Users\macie\ProblemPlecakowy\Data\f3_l-d_kp_4_20")
ka = KnapsackAlgorithm(items, capacity)
best_solution = ka.evolve()
print("Best Solution:", best_solution)


