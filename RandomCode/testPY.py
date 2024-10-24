from functools import reduce
import sys

arr = []
arrb = [1, 2, 3, 4, 5, 6]
sum = 0


def myMult(n):
    return lambda a: lambda b: print(f"a: %d, b: %d, n: %d and mult: %d"% (a, b, n, a*b*n))

myMult(3)(7)(10)

x = int(input("Enter one value"))
print(x, type(x))

def cumulative_sum(arr):
    return [reduce(lambda acc, x: acc + [acc[-1] + x] if acc else [x], arr, [])[i] for i in range(len(arr))]

# Example usage
input_array = [1, 2, 3, 4, 5]
# output_array = cumulative_sum(input_array)
# print(output_array)  # Output: [1, 3, 6, 10, 15]
print([reduce(lambda a, b: a + [a[-1]+b] if a else [b], input_array, [])[i] for i in range(len(input_array))])

x = 1
print(x<<3)
