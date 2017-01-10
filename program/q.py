def func1(name):
    f = open(name, 'r', encoding = 'utf-8')
    words = f.read().replace('\n', ' ').split()
    f.close()
    for i, word in enumerate(words) :
        words[i] = word.lower().strip('.,/1234567890@#$%^&*>»«<~`|\}{][!?():;-_=+"\'')
    return words

def func2(n, words):
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

def main():
    words = func1('file.txt')
    n = int(input('insert the number of syllables:\n'))
    l = func2(n, words)
    for elem in l:
        print(elem)
main()
