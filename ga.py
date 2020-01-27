from dataclasses import dataclass


@dataclass
class Conf:
    p_mutation: float = 0.001
    size: int = 100
    iterations: int = 500
    non_imp_runs: int = -1
    p_mutation_inc: float = 0.0001


class GA:
    def __init__(self, data):
        self.data = data
        self.conf = Conf()

        self.population = []
        self.scores = []

        self.best_score = 0
        self.best_ind = None

    def parent_selection(self, population):
        raise NotImplementedError

    def fitness(self, ind) -> float:
        raise NotImplementedError

    def mutation(self, population):
        raise NotImplementedError

    def crossover(self, ind1, ind2):
        raise NotImplementedError

    def selection(self, population, scores):
        raise NotImplementedError

    def _iteration(self):
        parents = self.parent_selection(self.population)
        assert all(len(p) == 2 for p in parents), "Wrong parents selection, each item should be an individuals pair"

        for ind1, ind2 in parents:
            offspring = self.crossover(ind1, ind2)
            if not isinstance(offspring, (list, tuple, set)):
                offspring = [offspring]

            self.population.extend(offspring)

        self.population = self.mutation(self.population)

        self.scores = [self.fitness(ind) for ind in self.population]

        self.population = self.selection(self.population, self.scores)

        # TODO: refactor
        self.scores = [self.fitness(ind) for ind in self.population]

        score, best = max(zip(self.scores, self.population), key=lambda el: el[0])
        if score > self.best_score:
            print(f"New best score: {score}")
            self.best_score = score
            self.best_ind = best[:]

    def run(self, init_population: list):
        self.population = init_population

        non_imp_runs = 0

        for i in range(self.conf.iterations):
            base_score = self.best_score

            self._iteration()

            print('.', end='')

            if self.best_score > base_score:
                non_imp_runs = 0
                # TODO: replace with initial
                self.conf.p_mutation = 0
            else:
                non_imp_runs += 1
                if self.conf.p_mutation < 0.001:
                    self.conf.p_mutation += self.conf.p_mutation_inc

            if self.conf.non_imp_runs >= 0 and non_imp_runs == self.conf.non_imp_runs:
                print(f"No improvement for last {non_imp_runs} generations")
                break

        print(f"Best score: {self.best_score} ({self.best_ind})")
