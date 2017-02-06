# Вариант №6

import re

def reading(name):
    f = open(name, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    return text

def find(text):
    r = re.search('\<td[^а-яА-Я]*Отряд:[^а-яА-Я]*([а-яА-Я]+)', text)
    order = '' 
    if r:
        order = r.group(1)
    return order

def record(order):
    f = open(input('Введите, пожалуйста, название файла вывода:\n'), 'a', encoding = 'utf-8')
    f.write(order + ' ') # Чтобы не слипалось при дописывании
    f.close()
    
def main():
    text = reading(input('Введите, пожалуйста, название файла ввода:\n'))
    order = find(text)
    record(order)
    
if __name__ == '__main__':
    main()
