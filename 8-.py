

from itertools import islice
import pdb


class Fib():
    def __init__(self):
        self.a, self.b = 1, 1

    def __iter__(self):
        while True:
            yield self.a
            self.a, self.b = self.b, self.a + self.b



for x in islice(Fib(), 1, 20):
    print(x)
pdb.set_trace()
