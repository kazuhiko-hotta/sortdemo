class InsertionSort:
    def __init__(self, data):
        self.data = data

    def sort(self):
        n = len(self.data)
        steps = 0
        for i in range(1, n):
            key = self.data[i]
            j = i - 1
            
            steps += 1
            yield [i, j], steps

            while j >= 0 and key < self.data[j]:
                steps += 1
                self.data[j + 1] = self.data[j]
                j -= 1
                yield [j + 1, i], steps
            
            self.data[j + 1] = key
            yield [j + 1], steps
