import heapq

class HeapItem:
    def __init__(self, item, min_heap=False):
        self.item = item
        self.min_heap = min_heap

    def __lt__(self, other):
        if self.min_heap:
            return self.item[0] < other.item[0]
        return self.item[0] > other.item[0]

class Heap:
    def __init__(self, min_heap=False):
        self.heap = []
        self.min_heap = min_heap

    def push(self, item):
        wrapped_item = HeapItem(item, self.min_heap)
        heapq.heappush(self.heap, wrapped_item)

    def pop(self):
        wrapped_item = heapq.heappop(self.heap)
        return wrapped_item.item

    def peek(self):
        return self.heap[0].item if self.heap else None

    def __len__(self):
        return len(self.heap)