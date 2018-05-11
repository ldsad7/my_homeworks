# Мой бот работает в телеграме по адресу @LdsadBot
# -*- coding: utf-8 -*-
import flask
import telebot
import conf
import json
from pymorphy2 import MorphAnalyzer
import random

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
morph = MorphAnalyzer()
with open('/home/ldsad/mysite/lemmas.json', 'r', encoding='utf-8') as f:
    lemmas = json.load(f)
for key in lemmas.keys(): # множества не сериализуются json
    lemmas[key] = set(lemmas[key])

bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

def invert_message(message):
    message = message.text
    words = message.split()
    result = ''
    titles = []
    before = []
    after = []
    for i, word in enumerate(words):
        new_word = word.strip('.,><|][);(:«»?"+=_0123456789-!@#$%^&*\\-—')
        if new_word == '':
            before.append('')
            after.append('')
            titles.append('')
            if i != len(words)-1:
                result += word + ' '
            else:
                result += word
            continue

        if new_word.capitalize() == new_word: # чтобы восстановить слова с заглавной буквы
            titles.append(1)
        elif new_word.upper() == new_word: # слова, написанные капсом
            titles.append(-1)
        else : # если человек пишет лесенкой типа "аБрАкАдАбРа", то я привожу к строчным буквам, т.к. не понятно, как восстанавливать
            titles.append(0)
        index_before = word.index(new_word[0])
        index_after = word.rindex(new_word[-1])
        before.append(word[:index_before])
        after.append(word[index_after+1:])
        parsed_word = morph.parse(new_word)[0]
        pos = parsed_word.tag.POS
        grams = str(parsed_word.tag).split(',')
        dop = set()
        for elem in grams:
            if ' ' in elem:
                grams.remove(elem)
                grams.extend(elem.split())

        for elem in 'sing, plur, nomn, gent, datv, accs, ablt, loct, voct, gen1, gen2, acc2, 1per, 2per, 3per, loc1, loc2, pres, past, futr, indc, impr, incl, excl, actv, pssv'.split(', '):
            if 'NPRO' in grams and (elem == '1per' or elem == '2per' or elem == '3per' or elem == 'sing' or elem == 'plur'):
                continue
            if (word == 'некто' or word == 'нечто') and elem == 'nomn':
                continue
            if elem in grams:
                dop.add(elem)
                grams.remove(elem)
        st = lemmas[grams[0]]
        for gram in grams[1:]:
            st = st & lemmas[gram]
        if st == set(): # если именно таких случаев по каким-то причинам не нашлось, то оставляем слово таким же
            if i != len(words)-1:
                result += word + ' '
            else:
                result += word
            continue

        while True:
            final_word = random.sample(st, 1)[0]
            prog = morph.parse(final_word)[0]
            if prog.score <= 0.5: # слишком ненадёжно, и поэтому вызывает ошибки
                continue
            if prog.tag.POS != pos:
                print(pos, prog.tag.POS)
                continue
            break

        final_word = prog.inflect(dop).word
        if titles[i] == -1:
            final_word = final_word.upper()
        elif titles[i] == 1:
            final_word = final_word.capitalize()
        final_word = before[i] + final_word + after[i]
        if i != len(words)-1:
            result += final_word + ' '
        else:
            result += final_word
    return result

app = flask.Flask(__name__)

# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Этот бот разговаривает с тобой, дублируя структуру твоего предложения, но заменяя слова на соответствующие по грамматическим характеристикам. Попробуй! Нужно просто ввести предложение (или текст).")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует на все прочие сообщения
def send_inverted(message):
    inverted_message = invert_message(message)
    bot.send_message(message.chat.id, inverted_message)

# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
