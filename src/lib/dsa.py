from collections import namedtuple

Point = namedtuple("Point", "x, y")


class UnionFind:
    def __init__(self):
        self.group_id = 0
        self.group = {}
        self.id = {}

    def union(self, a: int, b: int) -> None:
        A, B = a in self.id, b in self.id
        if A and B and self.id[a] != self.id[b]:
            self._merge(a, b)
        elif A or B:
            self._add(a, b)
        else:
            self._create(a, b)

    def _merge(self, a: int, b: int) -> None:
        obs, targ = sorted((self.id[a], self.id[b]), key=lambda i: len(self.group[i]))
        for node in self.group[obs]:
            self.id[node] = targ
        self.group[targ] |= self.group[obs]
        del self.group[obs]

    def _add(self, a: int, b: int) -> None:
        a, b = (a, b) if a in self.id else (b, a)
        targ = self.id[a]
        self.group[targ] |= {b}
        self.id[b] = targ

    def _create(self, a: int, b: int) -> None:
        self.group[self.group_id] = {a, b}
        self.id[a] = self.id[b] = self.group_id
        self.group_id += 1
