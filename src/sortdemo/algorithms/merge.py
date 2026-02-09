class MergeSort:
    def __init__(self, data):
        self.data = data
        self.steps = 0

    def sort(self):
        yield from self._merge_sort(0, len(self.data) - 1)

    def _merge_sort(self, l, r):
        if l < r:
            m = l + (r - l) // 2
            yield from self._merge_sort(l, m)
            yield from self._merge_sort(m + 1, r)
            yield from self._merge(l, m, r)

    def _merge(self, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        
        L = self.data[l:m+1]
        R = self.data[m+1:r+1]
        
        i = 0
        j = 0
        k = l
        
        while i < n1 and j < n2:
            self.steps += 1
            yield [k], self.steps
            
            if L[i] <= R[j]:
                self.data[k] = L[i]
                i += 1
            else:
                self.data[k] = R[j]
                j += 1
            k += 1
            
        while i < n1:
            self.steps += 1
            yield [k], self.steps
            self.data[k] = L[i]
            i += 1
            k += 1
            
        while j < n2:
            self.steps += 1
            yield [k], self.steps
            self.data[k] = R[j]
            j += 1
            k += 1
