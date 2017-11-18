'''
Социолингвистика: выберите верный вариант, укажите ваши данные
На сайте должны быть:

Главная страница (127.0.0.1), на которой показывается анкета с полями. Данные, которые будут вводиться в анкету, должны записываться в файл.

Страница статистики (127.0.0.1/stats), на которой результаты должны систематизироваться и в удобном виде выводиться на экран (это могут быть таблицы, какие-то подсчеты и тд).

Страница с выводом всех данных (127.0.0.1/json), на которой возвращается json со всеми введенными на сайте данными.

Страница поиска (127.0.0.1/search) и результатов поиска (127.0.0.1/results) . В ней достаточно сделать одно-два поля поиска (например, текстовый ввод и чекбокс или два текстовых ввода или другое). На странице должно быть описано, по каким данным ведется поиск.
'''

from flask import Flask, render_template, url_for, request, redirect
import re

app = Flask(__name__)

@app.route('/')
def questionnaire():
    return render_template('questionnaire.html')

@app.route('/answers1')
def get_answers1():
    d = request.args
    global i
    with open('data1.txt', 'a', encoding="utf-8") as f:
        i += 1
        f.write('{}. '.format(i))
        fl = 0
        for key in sorted(d.keys()):
            if fl != 0:
                f.write(', ')
            fl = 1
            f.write(key + ': ' + d[key] + '')
        f.write('.\n')

    return redirect(url_for('questions'))

@app.route('/answers2')
def get_answers2():
    d = request.args
    global j
    with open('data2.txt', 'a', encoding="utf-8") as f:
        j += 1
        f.write('{}. '.format(j))
        fl = 0
        for key in sorted(d.keys()):
            if fl != 0:
                f.write(', ')
            fl = 1
            f.write(key + ': ' + d[key] + '')
        f.write('.\n')

    return redirect(url_for('questionnaire'))
                        

@app.route('/questions')
def questions():
    return render_template('true_questionnaire.html')

@app.route('/stats')
def statistics():
    d = {}
    with open('data1.txt', 'r', encoding="utf-8") as f:
        lines1 = f.readlines()
    with open('data2.txt', 'r', encoding="utf-8") as g:
        lines2 = g.readlines()
    for k in range(len(lines1)):
        t = re.findall('username: (.*?)\.', lines1[k])
        s = re.findall('.+?. (.*?)\.', lines2[k])
        d[t[0]] = s[0].split(',')
        for n, elem in enumerate(d[t[0]]):
            d[t[0]][n] = elem.split(': ')
    return render_template('statistics.html', dic=d)

if __name__ == '__main__':
    i = 0
    j = 0
    app.run(debug=True)
