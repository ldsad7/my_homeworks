#Подобие таблицы:
n = float(input('Введите любое число\n'))
print('число | ', n)
for i in range(9 + len(str(round(n * 10, 3)))) :
    print('-', end = '')
print()
for i in range(1,11) :
    if i != 10 :
        print(i, '    | ', round(i * n, 3), end = '\n')
    else :
        print(i, '   | ', round(i * n, 3), end = '\n')
#Просто 10 строчек:
n = float(input('Введите любое число\n'))
for i in range(1,11) :
    print(i, '*', n, '=', i * n, end = '\n')
