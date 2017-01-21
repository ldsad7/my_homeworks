# Вариант №6

import random

# функция, считывающая словарь из csv-файла
def func1(name):
    dic = dict()
    f = open(name, 'r')
    for line in f.readlines():
        words = line.replace('\n', '').split(';')
        dic[words[0]] = words[1:] # мой csv-файл так организован
    return dic

def func2():
    n = int(input('Сколько раз Вы хотите угадывать слово? Введите ниже число >= 5:\n'))
    while n < 5:
        n = int(input('Введённое число < 5. Пожалуйста, введите число >= 5:\n'))
    return n

def func3(dic, n):
    for i in range(n):
        key = random.choice(list(dic.keys()))
        m = 3 
        print(i + 1, '-ое слово. ', 'Подсказка: ', random.choice(dic[key]), ' ...', sep = '')
        fl = 0
        while fl != 1 and m != 0:
            print('Попыток осталось: ', m, sep = '')
            if input('Введите ниже ваш ответ:\n').lower() == key:
                fl = 1
                print('Молодец! Всё верно!')
            else:
                print('Неверно. ', end = '')
                if m != 1:
                    print('Ещё одна подсказка: ', random.choice(dic[key]), ' ...', sep = '')
            m -= 1
        if fl == 0:
            print('Вы не угадали. Правильный ответ: ', key, sep = '') 

def main():
    dic = func1(input('Введите, пожалуйста, название файла:\n'))
    n = func2()
    func3(dic, n) # веселиться!

main()
