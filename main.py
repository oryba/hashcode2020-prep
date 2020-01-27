import random

from solvers import *

random.seed('1')

inputs = {
    "a_example": Dynamic,
    "b_small": Dynamic,
    "c_medium": Dynamic,
    "d_quite_big": Simple,
    "e_also_big": Simple
}

for inp, solver in inputs.items():
    print(f"Solving {inp} with {solver}...")

    s = solver(inp)
    score, res = s.start()

    print(f"Best: {score}\n")
