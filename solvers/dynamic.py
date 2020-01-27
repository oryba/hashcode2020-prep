from dataclasses import dataclass
from functools import lru_cache

from alg import Alg


@dataclass
class Solution:
    w: int
    slices: tuple


class Dynamic(Alg):
    CALLS = 0

    @lru_cache(None)
    def solve(self, W, I) -> tuple:
        self.CALLS += 1
        if I == 0:
            return 0, ()
        else:
            w = self.data.slices[I]
            if W < w:
                return self.solve(W, I - 1)
            else:
                s1 = self.solve(W, I - 1)
                s2 = self.solve(W - w, I - 1)
                if s1[0] < s2[0] + w:
                    return s2[0] + w, (*s2[1], I - 1)
                else:
                    return s1

    def start(self):
        self.data.slices.insert(0, 0)

        res = None

        # p0 = self.data.N * self.data.M
        # pd = p0 // 1000

        for i in range(1, self.data.N + 1):
            for w in range(self.data.M + 1):
                # if sum(D.slices[:i + 1]) <= w:
                res = self.solve(w, i)
                # if pd and (i * self.data.M + w) % pd == 0:
                #     print('.', end='')

        self.write(res[1])

        # print(f"Calls over dimension: {self.CALLS / p0 * 100}")

        return res
