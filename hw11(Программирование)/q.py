# Вариант №6

import re

def reading(name):
    f = open(name, 'r', encoding = 'utf-8')
    text = f.read()
    f.close()
    return text

def correction(text):
    corrected_text = re.sub('(Ф|ф)инлянди( |я(х|(ми?))?|и|й|ю|е(й|ю))', '\\1@алайзи\\2', text) # В моём файле не встречается Ф@а<...> или ф@а<...> в тексте
    corrected_text = re.sub('ФИНЛЯНДИ( |Я(Х|(МИ?))?|И|Й|Ю|Е(Й|Ю))', 'МАЛАЙЗИ\\1', corrected_text)
    corrected_text = corrected_text.replace('Ф@', 'М') 
    corrected_text = corrected_text.replace('ф@', 'м')
    return corrected_text

def recording(text):
    f = open(input('Введите, пожалуйста, название файла вывода:\n'), 'w', encoding = 'utf-8')
    f.write(text)
    f.close()

def main():
    text = reading(input('Введите, пожалуйста, название файла ввода:\n')) # файл называется Finland.html
    corrected_text = correction(text)
    recording(corrected_text)

if __name__ == '__main__':
    main()
