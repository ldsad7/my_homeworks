import re
import os
import csv

def printing(d1, d2):
    f = open('output1.txt', 'w', encoding = 'cp1251')
    for key, value in sorted(d1.items()):
        f.write(key + '\t' + str(value) + '\n')
    f.close()
    with open('output2.csv', 'w', encoding = 'cp1251') as csv_file:
        writer = csv.writer(csv_file, delimiter = ';')
        writer.writerow(['Название файла', 'Автор', 'Дата создания текста'])
        for key, value in sorted(d2.items()):
            lst = [str(key), str(value[0]), str(value[1])]
            writer.writerow(lst)
    

def dictionary(name):
    d1 = {}
    d2 = {}
    arr = []
    for file in os.listdir(name):
        with open(os.path.join(name, file), 'r', encoding = 'cp1251') as text:
            text = text.read()
            a = re.findall('<w>(.*?)</w>', text)
            d1[file] = len(a)
            b = re.findall('<meta content="(.*?)" name="author"', text)
            c = re.findall('<meta content="(.*?)" name="created"', text)
            d2[file] = b + c
            words = re.findall('<w><.*?>(.*?)</w>', text)
            d = re.findall('gr="A.*?gen.*?></ana>(.*?)</w>\s<w>.*?gr="S.*?gen.*?></ana>(.*?)</w>', text)
            arr.extend(d)
    print(arr)
    return d1, d2, arr

def main():
    d1, d2, d3 = dictionary('news')
    
    printing(d1, d2)
    

if __name__ == '__main__':
    main()
