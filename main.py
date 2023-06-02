import random
import numpy as np
import sys

import detect
import funcs

sys.setrecursionlimit(10 ** 7) # 최대 재귀 호출 수 조절

code = """
def func(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = []
    middle = []
    right = []
    for x in arr:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
        else:
            middle.append(x)
    
    return func(left) + middle + func(right)
"""

modified_code = funcs.modify_code(code)
print('--------------')
print(modified_code)
print('--------------')

exec(modified_code)

# 도출된 값을 바탕으로 샘플링 후 그래프 형태로 나타내기

x = []
y = []
for i in range(200, 10200, 200):
    operate_count = 0
    test_time = 100
    for n in range(test_time):
        ran_list = [random.random() * 1000 for _ in range(i)]
        exec("func(ran_list)")
    x.append(i)
    y.append(operate_count / test_time)

# for i in range(1, 101):
#     operate_count = 0
#     result = exec('func(i)')
#     x.append(i)
#     y.append(operate_count)

detect.detect_trend(np.array(x), np.array(y))
