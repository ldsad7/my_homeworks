def func(name) :
    f = open(str(name), 'r', encoding = 'utf-8')
    words = f.read().replace('\n', ' ').split(' ')
    f.close()
    return words
words = func('file.txt')
kol = 0
for i, word in enumerate(words) :
    words[i] = word.lower().strip('.,/1234567890@#$%^&*><~`|\}{][!?():;-_=+"')
    kol += 1
print('number of words =', kol)
