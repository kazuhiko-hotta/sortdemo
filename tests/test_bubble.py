from sortdemo.algorithms.bubble import BubbleSort

def test_bubble_sort():
    data = [4, 3, 2, 1]
    sorter = BubbleSort(data)
    # ジェネレータを最後まで回す
    for _ in sorter.sort():
        pass
    assert data == [1, 2, 3, 4]

def test_bubble_sort_empty():
    data = []
    sorter = BubbleSort(data)
    for _ in sorter.sort():
        pass
    assert data == []

def test_bubble_sort_already_sorted():
    data = [1, 2, 3, 4]
    sorter = BubbleSort(data)
    for _ in sorter.sort():
        pass
    assert data == [1, 2, 3, 4]
