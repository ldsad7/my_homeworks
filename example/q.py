import re

def reading(name):
    f = open(name, 'r', encoding = 'utf-8')
    words = f.read().split(' ')
    f.close()
    return words

def cleaning(words):
    for i, word in enumerate(words) :
        words[i] = word.lower().strip('.,/1234567890@#$%^&*><~`|\}{][!?():;-_=+"\'')
    return words

def printing(words):
    l = []
    for word in words:
        if re.search('кот', word) and word not in l:
            l.append(word)
            print(word)

def main():
    words = reading(input('Введите, пожалуйста, название файла:\n'))
    words = cleaning(words)
    printing(words)
    
if __name__ == '__main__':
    main()
