import re
import os
import csv

def printing(d1, d2, arr):
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
    f = open('output3.txt', 'w', encoding = 'cp1251')
    for elem in arr:
        f.write(elem + '\n')
    f.close()

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
            words_punct = re.findall('<w><.*?></ana>(.*?)</w>([\s,.!123456790:;?""])', text)
            words = [words_punct[i][0] for i in range(len(words_punct))]
            puncts = [words_punct[i][1] for i in range(len(words_punct))]
            d = re.findall('gr="A.*?gen.*?></ana>(.*?)</w>\s<w>.*?gr="S.*?gen.*?></ana>(.*?)</w>', text)
            e = []
            for i, elem in enumerate(d):
                ind1 = words.index(elem[0])
                ind2 = words.index(elem[1])
                if ind2 - ind1 == 1:
                    t = ind1 - 1
                    while t >= 0 and puncts[t] not in '[.?!]':
                        t -= 1
                    k = ind2
                    while k <= len(words) - 1 and puncts[k] not in '[.?!]':
                        k += 1
                    s = ''
                    for p in range(t + 1, k):
                        if p != ind1 and p != ind2:
                            s += words[p] + puncts[p]
                        elif p == ind1:
                            s += '\t' + words[p] + puncts[p]
                        else:
                            s += words[p] + puncts[p] + 't'
                    e.append(s)
            arr.extend(e)
    return d1, d2, arr

def main():
    d1, d2, arr = dictionary('news')
    
    printing(d1, d2, arr)
    

if __name__ == '__main__':
    main()
