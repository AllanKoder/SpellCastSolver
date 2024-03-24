from spellCast.solver import SpellCastSolver
from spellCast.spellCastChecker import *
from spellCast.spellCast import *
from spellCast.heap import Heap


# solver = SpellCastChecker()


heap = Heap()

m = {
        "test": 1,
        "tes32":2,
}
heap.push((1, m))
heap.push((21, m))
heap.push((134, m))
heap.push((1324, m))

print(heap.pop())
print(heap.pop())
print(heap.pop())
print(heap.pop())
