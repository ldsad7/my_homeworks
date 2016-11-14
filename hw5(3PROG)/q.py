print('Введите 7 целых чисел')
arr = []
for i in range(1, 8) :
    print('Введите ', i, '-ое целое число', sep = '')
    arr.append(int(input()))
for i in range(7) :
    for j in range(arr[i]) :
        print('X', end = '')
    print()
