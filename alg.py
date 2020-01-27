from dataclasses import dataclass


@dataclass
class Data:
    M: int
    N: int
    slices: list


class Alg:
    def __init__(self, name):
        self.name = name
        self.data = self.read()

    def read(self):
        with open(f'input/{self.name}.in') as f:
            m, n = f.readline().split(' ')
            return Data(
                int(m),
                int(n),
                [int(s) for s in f.readline().split(' ')]
            )

    def write(self, result):
        with open(f'output/{self.name}.out', 'w') as f:
            f.writelines([
                str(len(result)), "\n",
                ' '.join([str(s) for s in result])
            ])

    def start(self):
        raise NotImplementedError
