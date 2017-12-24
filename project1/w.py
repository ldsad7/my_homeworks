# 1) в файле Readme.md в папке с проектом должна находиться ссылка на скачанные
# и обработанные файлы вашей газеты, лежащие одним архивом на Google Drive

import csv, os, re, html, requests

def crawler_of_articles(url_name):
    global start_lst, today, months
    url = url_name + articles_lst[start_lst]

    with requests.Session() as session:
        session.post(url)
        response = session.get(url)
        if url_name == 'http://old.zwezda.su':
            response.encoding = 'windows-1251'
        else:
            response.encoding = 'utf-8'
    html_ = response.text
    crawler_of_pages(html_)
    start_lst += 1

    if url_name == 'http://old.zwezda.su':
        regAuthor = re.compile('<STRONG>.*?([А-ЯЁ][а-яё]+ [А-ЯЁ]+)<\/STRONG>', re.DOTALL)
        if regAuthor.findall(html_):
            author = regAuthor.findall(html_)[0]
        else:
            author = ''
    else:
        regAuthor = re.compile('<strong>Текст:<\/strong>.*?([а-яА-ЯёЁ]+ ?[а-яА-ЯёЁ]*)', re.DOTALL)
        if regAuthor.findall(html_):
            author = regAuthor.findall(html_)[0]
        else:
            return 0
    
    if url_name == 'http://old.zwezda.su':
        regHeader = re.compile('<h1.*?>(.*?)<\/h1>', re.DOTALL)
        if regHeader.findall(html_):
            header = regHeader.findall(html_)[0]
        else:
            print('header', articles_lst[start_lst - 1])
            return 0
        name = header
        name = name.replace('?', '')
        inappropriate_signs = list(':/"<>|')
        for sign in inappropriate_signs:
            name = html.unescape(re.sub(sign, '', header))
    else:
        regHeader = re.compile('<h1 class="heading nocaps">(.*?)<\/h1>', re.DOTALL)
        if regHeader.findall(html_):
            header = regHeader.findall(html_)[0]
        else:
            return 0

    if url_name == 'http://old.zwezda.su':
        regThree = re.compile('<div class="date">.*?([0-9]{2}.[0-9]{2}.[0-9]{2}).*?([а-яА-ЯёЁ]+)', re.DOTALL)
        if regThree.findall(html_):
            three = regThree.findall(html_)[0]
            date = three[0]
            topic = three[1]
        else:
            print('three', articles_lst[start_lst - 1])
            return 0
        date = date.split('.')
        date[2] = '20' + date[2]
        year = str(date[2])
        date = '.'.join(date)
    else:
        regThree = re.compile('http:\/\/zwezda\.su\/(.*?)\/([0-9]{4}).*?\/([a-zA-Z\-.]+)', re.DOTALL)
        if regThree.findall(url):
            three = regThree.findall(url)[0]
            topic = three[0]
            year = three[1]
            name = three[2]
        else:
            return 0
        regDate = re.compile('<div class="date">.*?([0-9а-яА-ЯёЁ ]+)', re.DOTALL)
        if regDate.findall(html_):
            date = regDate.findall(html_)[0]
        else:
            return 0
        
        if date == 'Сегодня':
            date = today # переменная определена в главной функции
        elif date == 'Вчера':
            date = today.split('.')
            date[0] = str((int(date[0]) - 1) % 31)
            date = '.'.join(date)
        else:
            date = date.split()
            ind = months.index(date[1])
            date = '{:0>2}'.format(date[0]) + '.' + '{:0>2}'.format(ind+1) + '.' + year

    if url_name == 'http://old.zwezda.su':
        regText = re.compile('(<P>.*?<\/P>)', re.DOTALL)
        if regText.findall(html_):
            text_ = regText.findall(html_)
            text = ''
            for txt in text_:
                text += html.unescape(re.sub('<.*?>', '', txt)).strip()
        else:
            print('text', articles_lst[start_lst - 1])
            return 0
    else:
        regText = re.compile('<div class="text over">(.*?)<\/div>', re.DOTALL)
        if regText.findall(html_):
            text = regText.findall(html_)[0]
            text = html.unescape(re.sub('<.*?>', '', text)).strip()
        else:
            return 0


    # не хочу выносить код ниже в функцию, поскольку тогда придётся передавать все параметры    
    path = os.path.join('zwezda', 'plain', year, date.split('.')[1])
    path_mystem1 = os.path.join('zwezda', 'mystem-xml', year, date.split('.')[1])
    path_mystem2 = os.path.join('zwezda', 'mystem-plain', year, date.split('.')[1])

    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tкраевая\t%s\tЗВЕЗДА\t\t%s\tгазета\tРоссия\tПермский край\tru' \
          % (path, author, header, date, topic, url, year)
    lst = row.split('\t')
    
    with open(os.path.join('zwezda', 'metadata.csv'), 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\t')
        writer.writerow(lst)

    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.exists(path_mystem1):
        os.makedirs(path_mystem1)

    if not os.path.exists(path_mystem2):
        os.makedirs(path_mystem2)
    
    with open(os.path.join(path, name + '_' + str(start_lst-1) + '.txt'), 'w', encoding='utf-8') as f:
        f.write('@au {}\n'.format(author))
        f.write('@ti {}\n'.format(header))
        f.write('@da {}\n'.format(date))
        f.write('@topic {}\n'.format(topic))
        f.write('@url {}\n'.format(url))
        f.write('TEXT:\n')
        f.write(text)

    with open(os.path.join(path_mystem1, name + '_' + str(start_lst-1) + '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)

    with open(os.path.join(path_mystem2, name + '_' + str(start_lst-1) + '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    
    return len(text.split())

def crawler_of_pages(html_):

    regHrefsWith = re.compile('<a href="(\/.*?)"', re.DOTALL)
    hrefs_with = set(regHrefsWith.findall(html_))

    regHrefsWithout = re.compile('<a href="([^\/].*?)"', re.DOTALL)
    hrefs_without = set(regHrefsWithout.findall(html_))

    hrefs_without_new = set()
    for href in hrefs_without:
        if not re.search('http', href):
            hrefs_without_new.add('/' + href)
    
    hrefs = hrefs_with | hrefs_without_new

    for href in hrefs:
        if href.endswith('/') or re.search('razdel', href):
            if href not in pages_set:
                pages_lst.append(href)
                pages_set.add(href)
        else:
            if href not in articles_set:
                articles_lst.append(href)
                articles_set.add(href)

def mystem(dir_name):
    path = os.path.join('zwezda', dir_name)
    with open('input.txt', 'w', encoding='utf-8') as q:
        for d, dirs, files in os.walk(path):
            for f in files:
                path_ = os.path.join(d, f)
                with open(path_, 'r', encoding='utf-8') as g:
                    q.write(g.read() + ' ~ ')
                    
    os.system("mystem.exe -icd --format xml input.txt output.txt")

    with open('output.txt', 'r', encoding="utf-8") as q:
        texts = q.read().split('~')
        i = 0
        for d, dirs, files in os.walk(path):
            for f in files:
                path_ = os.path.join(d, f)
                with open(path_, 'w', encoding='utf-8') as g:
                    g.write(texts[i])
                i += 1
    
    os.remove('input.txt')
    os.remove('output.txt')

def today_():
    global pages_lst, months
    
    with requests.Session() as session:
        session.post('http://zwezda.su' + pages_lst[start_page])
        response = session.get('http://zwezda.su' + pages_lst[start_page])
    html_ = response.text
    
    regToday = re.compile('<div class="today hidden-xs">.*?([0-9а-яА-ЯёЁ ]+)', re.DOTALL)
    today = regToday.findall(html_)[0].split()
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    ind = months.index(today[1])
    
    return '{:0>2}'.format(today[0]) + '.' + '{:0>2}'.format(ind+1) + '.2017'

def recording(page):
    global pages_lst, start_page
    while start_page < len(pages_lst): # считаем все ссылки
        with requests.Session() as session:
            session.post(page + pages_lst[start_page])
            response = session.get(page + pages_lst[start_page])
        html_ = response.text
        start_page += 1
        print(start_page, len(pages_lst))
        crawler_of_pages(html_)

def create_dirs():
    if not os.path.exists('zwezda'):
        os.makedirs('zwezda')
    
    if not os.path.exists(os.path.join('zwezda', 'plain')):
        os.makedirs(os.path.join('zwezda', 'plain'))
    
    if not os.path.exists(os.path.join('zwezda', 'mystem-xml')):
        os.makedirs(os.path.join('zwezda', 'mystem-xml'))
    
    if not os.path.exists(os.path.join('zwezda', 'mystem-plain')):
        os.makedirs(os.path.join('zwezda', 'mystem-plain'))
    
    with open(os.path.join('zwezda', 'metadata.csv'), 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter = '\t')
        writer.writerow('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage'.split('\t'))

def main():
    global pages_lst, pages_set, start_page, articles_set, articles_lst, start_lst, today
    # pages -- это сборники новостей, а не конкретные статьи
    pages_set = {'/'} # сюда записываются все посещенные ссылки сборников
    pages_lst = ['/'] # постоянно пополняемый список ссылок на сборники
    start_page = 0 # индекс первой непрочитанной ссылки на сборник
    
    today = today_() #один раз считаем сегодняшнюю дату, чтобы "сегодня" или "вчера" автоматически форматировать далее в соответствующее число
    # articles -- это непосредственно статьи
    articles_set = set() # сюда записываются все посещенные ссылки статей
    articles_lst = [] # постоянно пополняемый список статей
    start_lst = 0 # индекс первой непрочитанной ссылки на статью

    recording('http://zwezda.su')

    create_dirs()
    
    num = 0 # число слов
    while num <= 100000 and start_lst < len(articles_lst): # второе условие на случай, если слов будет меньше 100 тыс.
        print(num)
        num += crawler_of_articles('http://zwezda.su')

    if num <= 100000: # если слов нашлось меньше 100 тыс.
        # обновляем множества и массивы, поскольку переходим на старую версию сайта со старыми новостями
        pages_set = {'/'} 
        pages_lst = ['/']
        start_page = 0
        
        articles_set = set()
        articles_lst = []
        start_lst = 0

        recording('http://old.zwezda.su')
        
        while num <= 100000: # теперь собираем слова до конца
            num += crawler_of_articles('http://old.zwezda.su')
            print(num)
            
    mystem('mystem-plain') # обрабатываем mystem-ом файлы
    mystem('mystem-xml') # обрабатываем mystem-ом файлы
    
if __name__ == '__main__':
    main()

