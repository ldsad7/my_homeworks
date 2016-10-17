#Вариант №6
#Предполагая, что числа должны быть вещественными, а частное -- целым числом, и
#что должны выполняться оба условия одновременно, решение будет таким:
a = float(input('enter the first number\n'))
b = float(input('enter the second number\n'))
c = float(input('enter the third number\n'))
if b == 0. :
    print('you can\'t divide by zero')
elif a % b == c and a / b == c :
    print('YES')
else :
    print('NO')
    
#Предполагая, что числа должны быть вещественными, а частное -- целым числом, и что
#нужно проверить выполнение каждого условия по отдельности, решение будет таким:
a = float(input('enter the first number\n'))
b = float(input('enter the second number\n'))
c = float(input('enter the third number\n'))
if b == 0. :
    print('you can\'t divide by zero')
else :
    if a % b == c :
        print('YES, a % b == c')
    else :
        print('NO, a % b != c')
    if a / b == c :
        print('YES, a / b == c')
    else :
        print('NO, a / b != c')
        
#Предполагая, что числа должны быть целыми и что должны выполняться оба условия
#одновременно, решение будет таким:
a = int(input('enter the first number\n'))
b = int(input('enter the second number\n'))
c = int(input('enter the third number\n'))
if b == 0 :
    print('you can\'t divide by zero')
elif a % b == c and a / b == c :
    print('YES')
else :
    print('NO')
    
#Предполагая, что числа должны быть целыми и что нужно проверить выполнение
#каждого условия по отдельности, решение будет таким:
a = int(input('enter the first number\n'))
b = int(input('enter the second number\n'))
c = int(input('enter the third number\n'))
if b == 0 :
    print('you can\'t divide by zero')
else :
    if a % b == c :
        print('YES, a % b == c')
    else :
        print('NO, a % b != c')
    if a / b == c :
        print('YES, a / b == c')
    else :
        print('NO, a / b != c')
