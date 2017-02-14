import re

def reading(name):
    f = open(name, 'r', encoding = 'utf-8')
    lines = f.readlines()
    f.close()
    return lines

def array(lines):
    text = ''.join(lines)
    text = re.sub('<body>((.|\n)*)</body>', '\\1', text)
    text = re.sub('<[wc](.*?)>(.*?)</[wc]>', '\\1 \\2', text)
    print(text)
    l = re.findall('lemma="(.*?)" type="(.*?)" (.*)', text)
    return l
    
def recording1(d, n):
    f = open(input('Введите, пожалуйста, название выходного файла\n'), 'a', encoding = 'utf-8')
    f.write(str(n) + '\n')
    for key in d.keys():
        f.write(key + '\n')
    f.close()

def recording2(d):
    f = open(input('Введите, пожалуйста, название выходного файла\n'), 'a', encoding = 'utf-8')
    # нужно поставить блок на такое же наименование
    for key, value in d.items():
        if re.search('l.f.*', key):
            f.write(key + ' - ' + str(value) + '\n')
    f.close()

def recording3(l):
    name = input('Введите, пожалуйста, название выходного файла в формате csv\n')
    # нужно заставить пользователя назвать файл с окончанием csv
    while not name.endswith('.csv'):
        name = input('Введите, пожалуйста, название выходного файла в формате csv\n') 
    f = open(name, 'a', encoding = 'utf-8')
    for i, elem in enumerate(l):
        f.write(elem[0] + ',' + elem[1] + ',' + elem[2] + '\n')
    f.close()

def dictionary(lines):
    d = {}
    for line in lines:
        r = re.search('lemma=".*" type="(.*)"', line)
        if r:
            key = r.group(1)
            if key in d:
                d[key] += 1
            else:
                d[key] = 1
    return d

def main():
    name = input('Введите, пожалуйста, название входного файла\n')
    lines = reading(name)
    n = len(lines)
    d = dictionary(lines)
    recording1(d, n)
    recording2(d)
    l = array(lines)
    recording3(l)
    
if __name__== '__main__':
    main()
