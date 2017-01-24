import re

def cleaning(words):
    for i, word in enumerate(words) :
        words[i] = word.lower().strip('.,/1234567890@#$%^&*><~`|\}{][!?():;-_=+"\'')
    return words

def reading(name):
    f = open(name, 'r', encoding = 'utf-8')
    words = f.read().replace('\n', ' ').split(' ')
    f.close()
    return words

def search(words):
    for word in words:
        if re.search('[бвгджзйклмнпрстфхцчшщъь]*[аеёиоуыэюя][бвгджзйклмнпрстфхцчшщъь]*[аеёиоуыэюя][бвгджзйклмнпрстфхцчшщъь]*[аеёиоуыэюя][бвгджзйклмнпрстфхцчшщъь]*', word):
            print(word)

def main():
    words = reading('file.txt')
    words = cleaning(words)
    search(words)
    
main()
