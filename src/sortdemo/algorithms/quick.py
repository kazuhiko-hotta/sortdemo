class QuickSort:
    def __init__(self, data):
        self.data = data
        self.steps = 0

    def sort(self):
        yield from self._quick_sort(0, len(self.data) - 1)

    def _quick_sort(self, low, high):
        if low < high:
            # Partition index
            pi_gen = self._partition(low, high)
            pi = yield from pi_gen
            
            yield from self._quick_sort(low, pi - 1)
            yield from self._quick_sort(pi + 1, high)

    def _partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        
        for j in range(low, high):
            self.steps += 1
            yield [j, high], self.steps
            
            if self.data[j] <= pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                yield [i, j], self.steps
        
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        yield [i + 1, high], self.steps
        return i + 1
