from flask import Flask, render_template, url_for, request, redirect, session
import requests, json, urllib.request, re, os, html

headers = {
    "Host": "www.dorev.ru",
    "Cookie":"XMMGETHOSTBYADDR213134210163=U1%3A+163.210.unused-addr.ncport.ru; XMMcms4siteUSER=1; XMMFREE=YES; XMMPOLLCOOKIE=XMMPOLLCOOKIE",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}

app = Flask(__name__)

@app.route('/')
def main_page():
    pageUrl = 'https://www.gismeteo.ru/weather-skopje-3253/'
    dic = download_page(pageUrl)
    return render_template('main_page.html', dic = dic)

def gram_feat():
    os.system("mystem.exe -icd --format json input.txt output.txt")

@app.route('/meduza')
def meduza():
    href = 'https://meduza.io/'
    page = requests.get(href)
    page.encoding = 'utf-8'
    html_ = page.text
    
    reSent = re.compile('>([А-ЯЁа-яё,!?."a-zA-Z—\-«»(\s|&nbsp);0-9]+?)<', re.DOTALL)
    sentences = reSent.findall(html_)

    full_sent = ''
    for sent in sentences:
        if len(sent.strip()) != 0:
            full_sent += sent.strip() + ' '
    
    full_sent = re.sub('(&nbsp)', ' ', full_sent)
    with open('input.txt', 'w', encoding="utf-8") as f:
        f.write(full_sent)
    converted = convert_sent()
    converted = converted.replace(u'\xa0', u' ').lower()
    for sep in list('—0123456789?!()«»,.'):
        converted = converted.replace(sep, '')
    
    words = converted.split()
    d_words = {}
    for word in words:
        if word not in d_words:
            d_words[word] = 1
        else:
            d_words[word] += 1

    popular = []
    dic = sorted(d_words.items(), key=lambda x: -x[1])
    fl = 0
    for elem in dic:
        popular.append(elem)
        fl += 1
        if fl > 9:
            break
    
    return render_template('meduza.html', sentences=converted, popular=popular)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/results')
def results():
    with open('results.txt', 'r', encoding="utf-8") as f:
        num = int(f.read().strip())
    return render_template('results.html', result=num)

@app.route('/get_answers')
def get_answers():
    lst = request.args.getlist('yat')
    answers = list('1101001110')
    num = 0
    for i, elem in enumerate(lst):
        if elem == answers[i]:
            num += 1
    with open('results.txt', 'w', encoding="utf-8") as f:
        f.write(str(num))
    return redirect(url_for('results'))

@app.route('/conversion')
def conversion():
    converted = convert_sent()
    return render_template('conversion.html', word=converted)
    
def convert_sent():
    gram_feat()
    converted_sent = ''
    with open('output.txt', 'r', encoding="utf-8") as f:
        data = json.loads(f.read())
    
    for k in range(len(data)):
        converted = []
        if 'analysis' in data[k]:
            word = data[k]['text']
            for num, elem in enumerate(data[k]['analysis']):
                lemma = elem['lex']
                if lemma in d.keys():
                    if lemma == word:
                        converted = d[lemma]
                    else:
                        vowels = list('аеёиоуыэюяй') # добавил также «й» (поскольку перед ним «и» также заменяется на i и после него также не идёт «ъ»)
                        # вычленим окончание и основу слова (хотя бы примерно)
                        for i in range(len(word)):
                            if i < len(word) and i < len(lemma):
                                if word[i] != lemma[i]:
                                    break
                        
                        stem = d[lemma][:i-1] # считаю, что основа преобразована праивльно (в соответствии со словарём); +1 букву на всякий случай
                        end = word[i-1:] # окончание вручную преобразовываю

                        converted_end = []
                        for ind, letter in enumerate(end):
                            if letter == "и" and ind < len(end)-1: # в случае «ии{гласный или й}» я заменяю на ii{гласный или й}, но вроде бы в РЯ таких слов нет
                                if end[ind+1] in vowels:
                                    converted_end.append('і')
                                else:
                                    converted_end.append(letter)
                            else:
                                converted_end.append(letter)
                            if ind == len(end) - 1 and end[ind] not in vowels + list('ьъ'): # вставляю в конец после согласного (кроме «й») «ъ»
                                converted_end.append('ъ')
                        
                        grams = elem['gr'].replace('=', ',').split(',') # для разных частей речи mystem по-разному разбивает и группирует, так что проще разбить по всем разделителям
                        
                        if 'S' in grams and 'ед' in grams and ('дат' in grams or 'пр' in grams): # как я понял, только «е» может заменяться на «ѣ»
                            if converted_end[-1] == 'е': # поскольку леммы в словаре нет, придётся брать 1 последнюю букву в качестве окончания (в S(дат|пр)ед окончание заканчивается на гласную и состоит максимум из 1 буквы (во всех склонениях))
                                converted_end[-1] = 'ѣ'
                        if 'S' in grams and 'мн' in grams and ('жен' in grams or 'сред' in grams) and ('вин' in grams or 'им' in grams): # окончания существительных на
                            if converted_end[-2:] == ['i', 'е'] or converted_end[-2:] == ['ы', 'е']:
                                converted_end[-1] = 'я'
                            elif converted_end[-4:] == ['i', 'е', 'с', 'я']:
                                converted_end[-3] = 'я'

                        if 'A' in grams and 'полн' in grams and 'мн' in grams and ('вин' in grams or 'им' in grams): # окончание ПОЛНЫХ прилагательных ед. числа (в мн. числе не может быть таких окончаний), которые могут стоять только в им. или вин. падеже, определяются из контекста
                            if k > 1: # слева есть слово? следующий слева это пробел с, возможно, знаком препинания
                                if 'analysis' in data[k-2]:
                                    for ind_, analys in enumerate(data[k-2]['analysis']):
                                        lst = data[k-2]['analysis'][ind_]['gr'].replace('=', ',').split(',')
                                        if 'S' in lst and 'мн' in lst and ('жен' in lst or 'сред' in lst):
                                            if converted_end[-2] == ['i', 'е'] or converted_end[-2:] == ['ы', 'е']:
                                                converted_end[-1] = 'я'
                                            elif converted_end[-4:] == ['i', 'е', 'с', 'я']:
                                                converted_end[-3] = 'я'
                            elif k < len(data)-2: # справа есть слово? следующий справа это пробел с, возможно, знаком препинания
                                if 'analysis' in data[k+2]:
                                    for ind_, analys in enumerate(data[k+2]['analysis']):
                                        lst = data[k+2]['analysis'][ind_]['gr'].replace('=', ',').split(',')
                                        if 'S' in lst and 'мн' in lst and ('жен' in lst or 'сред' in lst):
                                            if converted_end[-2] == ['i', 'е'] or converted_end[-2:] == ['ы', 'е']:
                                                converted_end[-1] = 'я'
                                            elif converted_end[-4:] == ['i', 'е', 'с', 'я']:
                                                converted_end[-3] = 'я'
                        converted = stem + ''.join(converted_end)
                else:
                    if word in d.keys(): # в словаре есть много слов, которые стоят в косвенной форме
                        converted = d[word]
                        break # если нашли подходящий разбор, сразу выходим
                    else:
                        # здесь печатается только последний из предложенный mystem-ом разборов (поскольку какой-то из промежуточных может быть в словаре)
                        if word.startswith('бес'): # приставки «без», «через», «чрез» всегда оканчиваются на «з» (безполезный, безтактный, безсонница, черезчуръ)
                            word= word[:2] + 'з' + word[3:]
                        elif word.startswith('чрес'):
                            word = word[:3] + 'з' + word[4:]
                        elif word.startswith('черес'):
                            word= word[:4] + 'з' + word[5:]
                        vowels = list('аеёиоуыэюяй') # добавил также «й» (поскольку перед ним «и» также заменяется на i и после также него не идёт «ъ»)
                        converted = []
                        for ind, letter in enumerate(word):
                            if letter == "и" and ind < len(word)-1: # в случае «ии{гласный или й}» я заменяю на ii{гласный или й}, но вроде бы в РЯ таких слов нет
                                if word[ind+1] in vowels:
                                    converted.append('і')
                                else:
                                    converted.append(letter)
                            else:
                                converted.append(letter)
                            if ind == len(word) - 1 and word[ind] not in vowels + list('ьъ'): # вставляю в конец после согласного (кроме «й») «ъ»
                                converted.append('ъ')
                        
                        grams = elem['gr'].replace('=', ',').split(',') # для разных частей речи mystem по-разному разбивает и группирует, так что проще разбить по всем разделителям
                        
                        if 'S' in grams and 'ед' in grams and ('дат' in grams or 'пр' in grams): # как я понял, только «е» может заменяться на «ѣ»
                            if converted[-1] == 'е': # поскольку леммы в словаре нет, придётся брать 1 последнюю букву в качестве окончания (в S(дат|пр)ед окончание заканчивается на гласную и состоит максимум из 1 буквы (во всех склонениях))
                                converted[-1] = 'ѣ'

                        if 'S' in grams and 'мн' in grams and ('жен' in grams or 'сред' in grams) and ('вин' in grams or 'им' in grams): # окончания существительных на
                            if converted[-2:] == ['i', 'е']:
                                converted[-2:] = ['i', 'я']
                            elif converted[-2:] == ['ы', 'е']:
                                converted[-2:] = ['ы', 'я']
                            elif converted[-4:] == ['i', 'е', 'с', 'я']:
                                converted[-4:] = ['i', 'я', 'с', 'я']
                        
                        if 'A' in grams and 'полн' in grams and 'мн' in grams and ('вин' in grams or 'им' in grams): # окончание ПОЛНЫХ прилагательных ед. числа (в мн. числе не может быть таких окончаний), которые могут стоять только в им. или вин. падеже, определяются из контекста
                            if k > 1: # слева есть слово?
                                if 'analysis' in data[k-2]:
                                    for ind_, analys in enumerate(data[k-2]['analysis']):
                                        lst = data[k-2]['analysis'][ind_]['gr'].replace('=', ',').split(',')
                                        if 'S' in lst and 'мн' in lst and ('жен' in lst or 'сред' in lst):
                                            if converted[-2] == ['i', 'е'] or converted[-2:] == ['ы', 'е']:
                                                converted[-1] = 'я'
                                            elif converted[-4:] == ['i', 'е', 'с', 'я']:
                                                converted[-3] = 'я'
                            elif k < len(data)-2: # справа есть слово?
                                if 'analysis' in data[k-2]:
                                    for ind_, analys in enumerate(data[k+2]['analysis']):
                                        lst = data[k+2]['analysis'][ind_]['gr'].replace('=', ',').split(',')
                                        if 'S' in lst and 'мн' in lst and ('жен' in lst or 'сред' in lst):
                                            if converted[-2] == ['i', 'е'] or converted[-2:] == ['ы', 'е']:
                                                converted[-1] = 'я'
                                            elif converted[-4:] == ['i', 'е', 'с', 'я']:
                                                converted[-3] = 'я'
                        
        else:
            converted = data[k]['text']
        converted = ''.join(converted)
        converted_sent += converted
    return converted_sent

@app.route('/get_word')
def get_word():
    word = request.args['word']
    with open('input.txt', 'w', encoding="utf-8") as f:
        f.write(word)
    return redirect(url_for('conversion'))

def download_page(pageUrl):
    page = urllib.request.urlopen(pageUrl)
    html_ = page.read().decode('utf-8')
    d = dict()

    regTime = re.compile('<time .*?>(.*?)</time>', re.DOTALL)
    regTemperature = re.compile('<span class="js_value tab-weather__value_l">(.*?)</span>', re.DOTALL)
    regFeelTemperature = re.compile('<span class="tab-weather__feel-value">(.*?)</span>', re.DOTALL)

    time = regTime.findall(html_)
    d['time'] = time[0].strip()
    temperature = regTemperature.findall(html_)
    temperature = re.sub(r'<.*?>', ' ', temperature[0], flags=re.DOTALL)
    d['temp'] = html.unescape(''.join(temperature.strip().split()))
    feel_value = regFeelTemperature.findall(html_)
    d['feel'] = html.unescape(feel_value[0].strip())
    return d

def get_dict():
    href = 'http://www.dorev.ru/ru-index.html'
    page = requests.get(href, headers=headers)
    page.encoding = 'windows-1251'
    html_ = page.text
    
    d = dict()

    regHref = re.compile('href=\"(ru-index\.html\?l=[a-f0-9]{2})\"', re.DOTALL)
    hrefs = regHref.findall(html_)

    for href in hrefs:
        href_ = 'http://www.dorev.ru' + '/' + href
        page = requests.get(href_, headers=headers)
        page.encoding = 'windows-1251'
        html_ = page.text
        regWords = re.compile('<td class=\"uu\">([а-яёА-ЯЁ&#0-9;]*?)<\/td><td><\/td><td class=\"uu\">([а-яёА-ЯЁ&#0-9;]*?)(?:<span class=\"u[0-9]\"><span class="u[0-9]">([а-яёА-ЯЁ&#0-9;]*?)<\/span><span class=\"u[0-9]\">\'?<\/span><\/span>([а-яёА-ЯЁ&#0-9;]*))?[^а-яёА-ЯЁ&#0-9;]', re.DOTALL)
        words = regWords.findall(html_)
        for word in words:
            d[word[0].lower()] = html.unescape(word[1] + word[2] + word[3]).lower()

    return d

if __name__ == '__main__':
    d = get_dict()
    app.run(debug = 'True')
