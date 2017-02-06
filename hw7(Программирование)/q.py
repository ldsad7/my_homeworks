# Вариант №6

# Способ №1

# функция, считывающая файл
def func1(name):
    # поскольку предложенный для тестирования файл в кодировке ANSI
    # и при попытке преобразования его в кодировку utf-8 в notepad++
    # появляются "x93" "x94" на месте некоторых знаков препинания,
    # то возникающие ошибки будем игнорировать, поскольку они не влияют на слова
    f = open(name, 'r', encoding = 'utf-8', errors = 'ignore') 
    words = f.read().replace('\n', ' ').split()
    f.close()
    for i, word in enumerate(words):
        words[i] = word.lower().strip('.”“,/1234567890@#$%^&*>»«<№~`|\}{][!?():;-_=+"\'')
    return words

# функция, которая считает частоту слова и удаляет упоминания слова из списка
def func3(words, word):
    fl = 0
    num = 0
    while fl != 1:
        # обрабатываем исключение
        try:
            ind = words.index(word)
        except ValueError:
            fl = 1
            continue
        num += 1
        words.pop(ind)
    print(word, ': frequency = ', num, sep = '')
    return words

def func2(words):
    prefix = 'omni'
    # prefix = input('Enter any prefix, please!')
    length = len(prefix)
    for word in words:
        if word.startswith(prefix) and length < len(word):
            words = func3(words, word)
            words = func3(words, word[length:])
            print('-------------------------------------')

def main():
    func2(func1('file.txt'))

main()

# Способ №2

# вызван тем, что список может потребоваться далее,
# так что удалять элементы нецелесообразно

# функция, считывающая файл
def func1(name):
    # поскольку предложенный для тестирования файл в кодировке ANSI
    # и при попытке преобразования его в кодировку utf-8 в notepad++
    # появляются "x93" "x94" на месте некоторых знаков препинания,
    # то возникающие ошибки будем игнорировать, поскольку они не влияют на слова
    f = open(name, 'r', encoding = 'utf-8', errors = 'ignore') 
    words = f.read().replace('\n', ' ').split()
    f.close()
    for i, word in enumerate(words):
        words[i] = word.lower().strip('.”“,/1234567890@#$%^&*>»«<№~`|\}{][!?():;-_=+"\'')
    return words

# функция, которая считает частоту слова и удаляет упоминания слова из списка
def func3(words, word):
    num = 0
    for elem in words:
        if elem == word:
            num += 1
    print(word, ': frequency = ', num, sep = '')

def func2(words):
    prefix = 'under'
    # prefix = input('Enter any prefix, please!')
    length = len(prefix)
    l = []
    for word in words:
        if word.startswith(prefix) and length < len(word) and word not in l:
            func3(words, word)
            func3(words, word[length:])
            print('-------------------------------------')
            l.append(word)

def main():
    func2(func1('file.txt'))

main()
