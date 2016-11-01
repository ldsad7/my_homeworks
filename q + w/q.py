a = 5
fl = 0
b = input('Попробуйте угадать число\n')
while b != str(a) :
    fl = 1
    b = input('Введите ещё одно число, попробуйте ещё раз\n')
    if b == '' :
        print('Ты, похоже, устал...')
        break
    elif int(b) == a :
        print('Ты угадал, молодец!')
        break
    elif int(b) > a :
        print('Слишком большое число...')
    else :
        print('Слишком малое число...')
if fl == 0 :
    print('Ты угадал!')

