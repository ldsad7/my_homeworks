import re, requests, matplotlib.pyplot as plt, matplotlib.ticker as ticker
from matplotlib import gridspec
import numpy as np

plt.rc('font', family='Verdana')

def func(tag):
    tags = ['adj', 'adv', 'v', 'conj', 'det', 'intj', 'n', 'num', 'pn', 'prep']
    lst = [] # список для уже добавленных тэгов (т.к. тэги могут повторяться)
    tag = tag.strip() # т.к. есть ' na'
    if tag not in lst:
        if tag in tags:
            if tag in d.keys():
                d[tag] += 1
            else:
                d[tag] = 1
            lst.append(tag)
        else:
            if tag[0] == 'n' or tag[:4] == 'prop': # prop. n. -- noun
                if 'n' in d.keys():
                    d['n'] += 1
                else:
                    d['n'] = 1
                lst.append('n')
            elif tag[0] == 'v':
                if 'v' in d.keys():
                    d['v'] += 1
                else:
                    d['v'] = 1
                lst.append('v')
            elif tag[:3] == 'dem' and len(tag) > 3: # случай 'dem. pn. this (when speaking of person(s) )' не обрабатывается из-за неоднозначности
                if tag[4:] in d.keys():
                    d[tag[4:]] += 1
                else:
                    d[tag[4:]] = 1
            elif tag[:4] == 'loc': # только наречие
                if 'adv' in d.keys():
                    d['adv'] += 1
                else:
                    d['adv'] = 1

def main(): 
    pageUrl = 'http://wiki.dothraki.org/Vocabulary' 
    text = download_page(pageUrl) 

    global d
    d = {}
    full = re.compile('(<dl>(?:<dd><i>.*?\.?.*?<\/i>.*?<\/dd>)*?<\/dl>)', re.DOTALL) 
    full = full.findall(text)
    
    tags = ['adj', 'adv', 'v', 'conj', 'det', 'intj', 'n', 'num', 'pn', 'prep']
    for j in range(len(full)-1): # -1, т.к. последний список -- это раздел с аббревиатурами
        elem = full[j]
        # pos -- parts of speech
        pos1_ = re.compile('(<dl>(?:<dd><i>.*?\..*?<\/i>.*?<\/dd>)+.*?<b>)', re.DOTALL) # тэги одного слова
        pos2_ = re.compile('(<b>.*?<\/b>.*?(?:<i>.*?\..*?<\/i>.*?<\/dd>(?:<dd>)?)+.*?<\/dl>)', re.DOTALL) # производные слова

        # Косяки в разметке, которые я обрабатываю:
        # 1) лишний пробел у 'ni' в одном случае (<dl><dd><i> ni.</i> magic)
        # Косяки в разметке, которые я не обрабатываю (можно поставить ноль мне из-за этого!):
        # 1) 'phrase' вместо части речи 
        # 2) adj без точки на конце (chak [t͡ʃak] adj silent)
        # 3) название части речи жирное! (тогда как в остальных случаях курсивное: <ul><li><b>naqis</b> [naˈqes] <span id="naqis"></span></li></ul><dl><dd><b>adj.</b> small</dd><dd><b>naqisat</b> <i>vin.</i> to be small</dd><dd><span style="color:gray"><small>past SG: <b>naqis</b></small></span></dd></dl>)
        # 4) 'dem. pn.' с точкой после dem
        # 5) слова без части речи (lekhaan enough, sufficiently)
        # 6) prefix (elided version of /me-/, a complementizer used to introduce subordinate clauses) (здесь нет точки)

        pos1 = pos1_.findall(elem)
        pos1_ = re.compile('<dd><i>(.*?)\..*?<\/i>.*?<\/dd>', re.DOTALL) # тэги одного слова
        
        if pos1 != []:
            pos1 = pos1[0]
            pos1 = pos1_.findall(pos1)
        else:
            pos1 = pos1_.findall(elem)

        pos2 = pos2_.findall(elem)
        
        if pos2 != []:
            pos2 = pos2[0]
            pos2_ = re.compile('(<b>[a-z A-Z]+<\/b>.*?(?:<i>.*?\..*?<\/i>.*?<\/dd>(?:<dd>)?)+)', re.DOTALL) # производные слова
            pos2 = pos2_.findall(pos2)
            
            pos2_ = re.compile('<i>(.*?)\..*?<\/i>', re.DOTALL)            
            for i in range(len(pos2)):
                pos2[i] = pos2_.findall(pos2[i])
                
        for tag in pos1:
            func(tag)
        for elmt in pos2:
            for tag in elmt:
                func(tag)

    dic = {}
    letters_ = re.compile('[^ ]<b>([a-z])[a-z]*?<\/b>', re.DOTALL) # ловим первую букву
    letters = letters_.findall(text)

    for letter in letters: # букв b и p, u, w, x в дотракийском алфавите нет
         if letter in dic:
             dic[letter] += 1
         else:
             dic[letter] = 1

    d = sorted(d.items(), key=lambda x: x[1])

    keys = [elem[0] for elem in d]
    values = [elem[1] for elem in d]

    ax1 = plt.subplot(121)
    ax1.set_xticklabels(keys)
    ax1.scatter(sorted(keys), sorted(values), c='dodgerblue', marker='X')
    ax1.set_title("Число слов данной части речи в словаре")
    ax1.set_ylim(0, 750)
    ax1.set_xlabel("Части речи")
    ax1.set_ylabel("Число слов данной части речи")
    
    plt.grid(True, color='black')

    dic = sorted(dic.items(), key=lambda x: x[1])
    keys_ = [elem[0] for elem in dic]
    values_ = [elem[1] for elem in dic]

    x = np.arange(len(keys_))
    ax2 = plt.subplot(122)
    ax2.bar(x, values_, align='center', tick_label='')
    ax2.set_xticks(x, values_)
    ax2.set_xticklabels(keys_, fontsize=9, minor=True)
    ax2.set_title("Число слов, начинающихся на данную букву, в словаре")
    ax2.set_ylim(0, 200)
    ax2.set_xlabel("Буквы дотракийского языка")
    ax2.set_ylabel("Число слов, начинающихся на данную букву")

    plt.show()

def download_page(pageUrl):
    with requests.Session() as session: 
        session.post(pageUrl) 
        response = session.get(pageUrl) 
    return response.text 

if __name__ == '__main__': 
    main()
