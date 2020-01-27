from functools import lru_cache

from alg import Alg


class Simple(Alg):
    CALLS = 0

    @lru_cache(None)
    def solve(self, W, I) -> tuple:
        global CALLS
        CALLS += 1
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
        res = []
        best = 0

        for j in range(self.data.N, 1, -1):
            loc_res = []
            loc_best = 0
            for i in range(j - 1, -1, -1):
                if loc_best + self.data.slices[i] > self.data.M:
                    continue
                loc_res.append(i)
                loc_best += self.data.slices[i]

            if loc_best > best:
                res = loc_res
                best = loc_best

        res = [self.data.N - i for i in res]
        self.write(res)

        return best, res
