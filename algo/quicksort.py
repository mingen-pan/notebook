from random import shuffle, randint


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


def partition(arr, lo, hi):
    if lo >= hi:
        return
    target = arr[lo]
    i, j = lo + 1, hi
    while True:
        while i <= hi and arr[i] <= target:
            i += 1
        while j > lo and arr[j] >= target:
            j -= 1
        if i >= j:
            break
        swap(arr, i, j)
    swap(arr, lo, j)
    partition(arr, lo, j - 1)
    partition(arr, j + 1, hi)


def quickSort(arr):
    shuffle(arr)
    partition(arr, 0, len(arr) - 1)
    return arr


def test(arr):
    quickSort(arr)
    ans = sorted(arr)
    for a, b in zip(ans, arr):
        if a != b:
            return False
    return True


def generator(start=0, end=1000000, size=10000):
    return [randint(start, end) for _ in range(size)]


if __name__ == '__main__':
    for i in range(10):
        arr = generator(1, 1000, 10000)
        if not test(arr):
            print("Fail")
            exit(1)
    print("PASS")
    exit(0)

