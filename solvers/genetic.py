import random

from alg import Alg
from ga import GA, Conf


class Genetic(Alg, GA):
    def parent_selection(self, population):
        parents = []

        i = 0

        while i < (self.conf.size - len(population)) // 2:
            parents.append(
                (random.choice(population),
                 random.choice(population))
            )
            i += 1

        return parents

    def fitness(self, ind) -> float:
        score = 0
        for i in range(self.data.N):
            if ind[i]:
                if score + self.data.slices[i] < self.data.M:
                    score += self.data.slices[i]
                else:
                    break
        return score

    def mutation(self, population):
        for ind in population:
            for i in range(self.data.N):
                if random.random() < self.conf.p_mutation:
                    ind[i] = not ind[i]
        return population

    def crossover(self, ind1, ind2):
        pc1 = random.randint(1, self.data.N - 1)
        pc2 = random.randint(1, self.data.N - 1)
        p1 = min(pc1, pc2)
        p2 = max(pc1, pc2)
        return [
            ind1[:p1] + ind2[p1:p2] + ind1[p2:],
            ind2[:p1] + ind1[p1:p2] + ind2[p2:],
            ind1[:p1] + ind1[p1:p2] + ind2[p2:],
            ind2[:p1] + ind2[p1:p2] + ind1[p2:],
            ind1[:p1] + ind2[p1:p2] + ind2[p2:],
            ind2[:p1] + ind1[p1:p2] + ind1[p2:]
        ]

    def selection(self, population, scores):
        return random.choices(population=population, k=self.conf.size, weights=[1] * len(population))

    def _prepare_output(self, result):
        score = 0
        output = []

        for i in range(self.data.N):
            if result[i]:
                if score + self.data.slices[i] < self.data.M:
                    score += self.data.slices[i]
                else:
                    break
                output.append(i)

        return output

    def start(self):
        self.conf = Conf(p_mutation=0.0001, size=200, iterations=3000)

        self.run(
            [[bool(random.randint(0, 1)) for i in range(self.data.N)] for j in range(20)]
        )

        res = self._prepare_output(self.best_ind)

        self.write(res)

        return self.best_score, res