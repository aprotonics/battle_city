import heapq


class PriorityQueue():
    def __init__(self):
        self._list = []
    
    def __repr__(self) -> str:
        return self._list.__repr__()
    
    def __len__(self) -> int:
        return self._list.__len__()
    
    def push(self, element: int, priority: int):
        heapq.heappush(self._list, (priority, element))

    def extract(self) -> int:
        return heapq.heappop(self._list)[1]
    
    def empty(self) -> bool:
        return not bool(self.__len__())


class SquareGrid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
    
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        (x, y) = id
        condition = ((id not in self.walls) and 
                ((x + 25, y) not in self.walls) and ((x, y + 25) not in self.walls) and
                ((x + 25, y + 25) not in self.walls))
        return condition

    def neighbours(self, id):
        (x, y) = id
        results = [(x, y-25), (x-25, y), (x, y+25), (x+25, y)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node): # Вычисление пути в зависимости от to_node
        return self.weights.get(to_node, 25)
