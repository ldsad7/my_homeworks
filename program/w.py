def func0(name):
    f = open(name, 'r', encoding = 'utf-8')
    words = f.read().replace('\n', ' ').split()
    f.close()
    for i, word in enumerate(words) :
        words[i] = word.lower().strip('.,/1234567890@#$%^&*>»«<~`|\}{][!?():;-_=+"\'')
    return words

def func1(n, words):
    vow = 'аеёиоуыэюя'
    l = []
    for word in words:
        num = 0
        for elem in word:
            if elem in vow:
                num += 1
        if num == n:
            l.append(word)
    return l

def func2(words, letter):
    l = []
    for word in words:
        if word.startswith(letter):
            l.append(word)
    return l

def main():
    numbers = '1234567890'
    name = input('Введите имя файла:\n')
    words = func0(name)
    key = input('Привет!\nВведи 1, если хочешь, чтобы программа вывела слова с заданным количеством слогов,\nили введи 2, если хочешь, чтобы программа вывела слова, начинающиеся на заданную букву:\n')
    while key not in numbers:
        key = input('Привет!\nПопробуй ещё раз!\nВведи 1, если хочешь, чтобы программа вывела слова с заданным количеством слогов,\nили введи 2, если хочешь, чтобы программа вывела слова, начинающиеся на заданную букву:\n')
    if int(key) == 1:
        n = int(input('Введите число требуемых слогов в слове:\n'))
        l = func1(n, words)
    else:
        letter = input('insert the first letter of words:\n').lower()
        l = func2(words, letter)
    for elem in l:
        print(elem)

main()
