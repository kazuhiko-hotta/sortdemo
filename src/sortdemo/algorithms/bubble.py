class BubbleSort:
    def __init__(self, data):
        self.data = data

    def sort(self):
        n = len(self.data)
        steps = 0
        for i in range(n):
            for j in range(0, n - i - 1):
                steps += 1
                # Yield current comparison indices
                yield [j, j + 1], steps
                
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    # Yield after swap
                    yield [j, j + 1], steps
