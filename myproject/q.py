from flask import Flask, render_template, url_for, request, redirect, session
import json, sqlite3, urllib.request, re
from sqlite3 import Error

#DATABASE = "C:\\Users\Эдуард\Desktop\myproject\pythonsqlite.sqlite"

app = Flask(__name__)

@app.route('/')
def main_page():
    pageUrl = 'https://www.gismeteo.ru/weather-skopje-3253/'
    dic = download_page(pageUrl)
    
    return render_template('main_page.html', dic = dic)

@app.route('/conversion')
def conversion():
    return render_template('conversion.html')

@app.route('/word')
def word():
    word = request.args['word']
    vowels = 'аеёиоуыэюя'.split()
    #lemma = mystem(word)
    return render_template('conversion.html', word=word)

def download_page(pageUrl):
    page = urllib.request.urlopen(pageUrl)
    html = page.read().decode('utf-8')
    d = dict()

    regTime = re.compile('<time .*?>(.*?)</time>', re.DOTALL)
    regTemperature = re.compile('<span class="js_value tab-weather__value_l">(.*?)</span>', re.DOTALL)
    regFeelTemperature = re.compile('<span class="tab-weather__feel-value">(.*?)</span>', re.DOTALL)

    time = regTime.findall(html)
    d['time'] = time[0].strip()
    temperature = regTemperature.findall(html)
    temperature = re.sub(r'<.*?>', ' ', temperature[0], flags=re.DOTALL)
    d['temp'] = ''.join(temperature.strip().split())
    feel_value = regFeelTemperature.findall(html)
    d['feel'] = feel_value[0].strip()
    return d

if __name__ == '__main__':
    app.run(debug="True")
