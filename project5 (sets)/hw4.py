import re, requests

def main():
    pageUrl = "https://news.yandex.ru/yandsearch?lr=213&cl4url=https%3A%2F%2Fura.news%2Farticles%2F1036273369&content=alldocs&stid=rIy9dEqR6pAf0S-W5HEu&from=story"
    html = download_page(pageUrl)
    regHref = re.compile('href=\"(http.*?)\"', re.DOTALL)
    hrefs = regHref.findall(html)
    aHrefs = []
    for href in hrefs:
        if not re.search('yandex', href):
            aHrefs.append(href)
    
    words_ = []
    sets_of_words = set()
    for href in aHrefs[:4]: # здесь можно поменять количество рассматриваемых ссылок
        result = words(href)
        words_.append(result)
        sets_of_words.add(frozenset(result))

    fl = 0
    common = set()
    different = set()
    for elem in sets_of_words:
        if fl == 0:
            common = elem
            different = elem
            fl = 1
        else:
            common &= elem
            different ^= elem

    more_than_one = set()
    for word in different:
        for elem in words_:
            if word in elem:
                if elem.index(word) != len(elem) - 1 - elem[::-1].index(word):
                    more_than_one.add(word)

    with open('common_words.txt', 'w', encoding='utf-8') as f: # Общие для всех пропагандистских заметок слова
        for word in sorted(common):
            f.write(word + '\n')

    with open('unique_words.txt', 'w', encoding='utf-8') as f: # Уникальные в пропагандистских заметках слова (т.е. встречающиеся только в одной из них)
        for word in sorted(different):
            f.write(word + '\n')

    with open('unique_words_more_than_one.txt', 'w', encoding='utf-8') as f: # Уникальные (встречаются только в одном тексте) в пропагандистских заметках слова с частотой >1
        for word in sorted(more_than_one):
            f.write(word + '\n')
    
def words(href):
    html = download_page(href)
    regWords = re.compile('([а-яА-ЯёЁ]+)', re.DOTALL)
    words = regWords.findall(html)
    words = [elem.lower() for elem in words]
    return words

def download_page(pageUrl):
    with requests.Session() as session: 
        session.post(pageUrl) 
        response = session.get(pageUrl)
    return response.text 
    
if __name__ == "__main__":
    main()
