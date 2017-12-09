# Анкета выложена по адресу www.vladisgrig.ru

from flask import Flask, render_template, url_for, request, redirect, session
import json, sqlite3
from sqlite3 import Error

#DATABASE = "C:\\Users\Эдуард\Desktop\myproject\pythonsqlite.sqlite" # путь для локального компьютера
DATABASE = "/home/eduard/myproject/pythonsqlite.sqlite" # путь для сервера

app = Flask(__name__)

app.secret_key = 'bF5w%C1s{ncdcdq8K?PAF9a*%o}ti0P#' # ключ для сервера

@app.route('/')
def questions0():
    return render_template('questionnaire1.html')

@app.route('/questions1')
def questions1():
    if 'userid' in session:
        return render_template('questionnaire2.html')
    else:
        return redirect(url_for('questions0'))

@app.route('/questions2')
def questions2():
    if 'userid' in session:
        return render_template('questionnaire3.html')
    else:
        return redirect(url_for('questions0'))

def get_lists():
    cities0 = ['сочи', 'пиза', 'казань', 'киев', 'санкт-петербург', 'чернобыль', 'челябинск', 'великий устюг'] # правильные ответы (не склоняет)
    cities1 = ['сочах', 'пизе', 'казани', 'киева', 'санкт-петербурга', 'чернобыле', 'челябинске', 'великого устюга'] # правильные ответы (склоняет)
    rivers0 = ['москва', 'волга', 'амур', 'лена']
    rivers1 = ['москве', 'волги', 'амура', 'лены']
    villages0 = ['ясная поляна', 'простоквашино']
    villages1 = ['ясной поляне', 'простоквашина']
    lakes0 = ['байкал']
    lakes1 = ['байкале']
    islands0 = ['исландия']
    islands1 = ['исландии']
    states0 = ['нью-йорк']
    states1 = ['нью-йорке']
    mountains0 = ['эльбрус']
    mountains1 = ['эльбрусе']
    peninsula0 = ['крым']
    peninsula1 = ['крыме']
    sierra0 = ['гималаи']
    sierra1 = ['гималаях']
    squares0 = ['лубянка']
    squares1 = ['лубянки']

    lst0 = [cities0, rivers0, villages0, lakes0, islands0, states0, mountains0, peninsula0, sierra0, squares0]
    lst1 = [cities1, rivers1, villages1, lakes1, islands1, states1, mountains1, peninsula1, sierra1, squares1]

    return lst0, lst1

@app.route('/finalpage')
def finalpage():
    all = 0 # общее число вопросов
    num = 0 # число правильных ответов

    lst0, lst1 = get_lists()
    
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM db1 WHERE id=?", [session['userid']])
    row = cur.fetchall()
    
    for i in range(1, len(row[0])):
        r = row[0][i].split(', ')
        for j in range(len(r)):
            low = r[j].lower()
            if low == lst0[i-1][j] or low == lst1[i-1][j]:
                num += 1
            all += 1

    return render_template('finalpage.html', num = num, all = all)

@app.route('/json')
def json_():
    with open('data1.txt', 'r', encoding="utf-8") as f:
        json1 = f.read()
    with open('data2.txt', 'r', encoding="utf-8") as f:
        json2 = f.read()
    with open('data3.txt', 'r', encoding="utf-8") as f:
        json3 = f.read()
    return render_template('json.html', json1=json1, json2=json2, json3=json3)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results(): # пока что почти никакой статистики: просто среднее значение;
    
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    ''' может понадобиться, если статистика будет обширней
    cur.execute("SELECT * FROM db0")
    rows0 = cur.fetchall()
    '''
    
    cur.execute("SELECT * FROM db1")
    rows1 = cur.fetchall()
    
    ''' может понадобиться, если статистика будет обширней
    cur.execute("SELECT * FROM db2")
    rows2 = cur.fetchall()
    '''

    cur.execute("SELECT * FROM db3")
    rows3 = cur.fetchall()

    search = list(rows3[-1]) # берём последний запрос

    phrases = search[0].split(', ')
    gend = search[1].split(', ')
    lage = int(search[2])
    rage = int(search[3])
    educ = search[4].split(', ')
    spec = search[5].split(', ')

    lst0, lst1 = get_lists()
    toponyms = ['city', 'countryside', 'river', 'lake', 'island', 'state', 'mountain', 'sierra', 'peninsula', 'square']

    all = 0 # общее число топонимов
    for ind, toponym in enumerate(toponyms):
        if toponym in phrases:
            all += len(lst0[ind])

    num_of_users = 0 # общее число носителей, удовлетворяющих выбранным характеристикам
    num = 0 # общее число случаев, когда пользователи с выбранными характеристиками просклоняли какой-нибудь топоним
    
    
    for i in range(len(rows1)): # берём только тех, кто прошёл вторую анкету
        id = rows1[i][0]
        cur.execute("SELECT * FROM db0 WHERE id = ?", [id])
        row0 = cur.fetchall()
        if row0[0][2] in gend and lage <= row0[0][3] <= rage and str(row0[0][6]) in educ and str(row0[0][7]) in spec:
            num_of_users += 1
            for ind, toponym in enumerate(toponyms):
                if toponym in phrases:
                    for elem in rows1[i][ind+1].split(', '):
                        if elem.lower() in lst1[ind]:
                            num += 1

    try:
        value = num / num_of_users
        return render_template('results.html', value = round(value, 3))
    except ZeroDivisionError:
        return render_template('results.html', value = 0)

@app.route('/stats1')
def stats1():
    conn = create_connection(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM db0")
    rows0 = list(cur.fetchall())
    
    conn.commit()
    return render_template('stats1.html', rows0 = rows0)

@app.route('/stats2')
def stats2():
    conn = create_connection(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM db1")
    rows1 = list(cur.fetchall())
    
    conn.commit()
    return render_template('stats2.html', rows1 = rows1)

@app.route('/stats3')
def stats3():
    conn = create_connection(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM db2")
    rows2 = list(cur.fetchall())
    
    conn.commit()
    return render_template('stats3.html', rows2 = rows2)

@app.route('/stats4')
def stats4():
    conn = create_connection(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM db3")
    rows3 = list(cur.fetchall())
    
    conn.commit()
    return render_template('stats4.html', rows3 = rows3)

@app.route('/answers1')
def get_answers1():
    username = request.args['username']
    gender = request.args['gender']
    age = request.args['age']
    language = request.args['language']
    education = request.args['education']
    specialization = request.args['specialization']
    cities = ', '.join(request.args.getlist('city'))

    conn = create_connection(DATABASE)
    with conn:
        db = (username, gender, age, language, cities, education, specialization)
        userid = create_db0(conn, db)
        session['userid'] = userid
        conn.commit()

    with open('data1.txt', 'a', encoding="utf-8") as f:
        json.dump([username, gender, age, language, cities, education, specialization], f, ensure_ascii = False)
    
    return redirect(url_for('questions1'))

@app.route('/answers2')
def get_answers2():
    cities = ', '.join(request.args.getlist('city'))
    rivers = ', '.join(request.args.getlist('river'))
    countrysides = ', '.join(request.args.getlist('countryside'))
    lake = request.args['lake']
    island = request.args['island']
    state = request.args['state']
    mountain = request.args['mountain']
    peninsula = request.args['peninsula']
    sierra = request.args['sierra']
    square = request.args['square']
    
    conn = create_connection(DATABASE)
    with conn:
        if 'userid' not in session:
            return redirect(url_for('questions0'))
        db = (session['userid'], cities, rivers, countrysides, lake, island, state, mountain, peninsula, sierra, square)
        create_db1(conn, db)
        conn.commit()

    with open('data2.txt', 'a', encoding="utf-8") as f:
        json.dump([session['userid'], cities, rivers, countrysides, lake, island, state, mountain, peninsula, sierra, square], f, ensure_ascii = False)

    return redirect(url_for('questions2'))
                        
@app.route('/answers3')
def get_answers3():
    cities = ', '.join(request.args.getlist('city'))
    rivers = ', '.join(request.args.getlist('river'))
    countryside = request.args['countryside']
    lake = request.args['lake']
    island = request.args['island']
    state = request.args['state']
    mountain = request.args['mountain']
    peninsula = request.args['peninsula']
    sierra = request.args['sierra']
    square = request.args['square']
    
    conn = create_connection(DATABASE)
    with conn:
        if 'userid' not in session:
            return redirect(url_for('questions0'))
        db = (session['userid'], cities, rivers, countryside, lake, island, state, mountain, peninsula, sierra, square);
        db_id = create_db2(conn, db)
        conn.commit()

    with open('data3.txt', 'a', encoding="utf-8") as f:
        json.dump([session['userid'], cities, rivers, countryside, lake, island, state, mountain, peninsula, sierra, square], f, ensure_ascii = False)
    
    return redirect(url_for('finalpage'))

@app.route('/answers4')
def get_answers4():
    phrases = ', '.join(request.args.getlist("phrase"))
    genders = ', '.join(request.args.getlist("gender"))
    lage = int(request.args['lage'])
    rage = int(request.args['rage'])
    education = ', '.join(request.args.getlist("education"))
    specialization = ', '.join(request.args.getlist("specialization"))

    conn = create_connection(DATABASE)
    with conn:
        db = (phrases, genders, lage, rage, education, specialization);
        create_db3(conn, db)
        conn.commit()
    
    return redirect(url_for('results'))

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)

def create_db0(conn, db):
    sql = ''' INSERT INTO db0(username, gender, age, language, city, education, specialization)
              VALUES(?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, db)
    conn.commit()
    return cur.lastrowid
    
def create_db1(conn, db):
    sql = ''' INSERT INTO db1(id, city, river, countryside, lake, island, state, mountain, peninsula, sierra, square)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, db)
    conn.commit()
    return cur.lastrowid

def create_db2(conn, db):
    sql = ''' INSERT INTO db2(id, city, river, countryside, lake, island, state, mountain, peninsula, sierra, square)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, db)
    conn.commit()
    return cur.lastrowid
        
def create_db3(conn, db):
    sql = ''' INSERT INTO db3(phrase, gender, lage, rage, education, specialization)
              VALUES (?, ?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, db)
    conn.commit()
    
if __name__ == '__main__':
    sql_create_questions0 = ''' CREATE TABLE IF NOT EXISTS db0 (
                                    id integer PRIMARY KEY,
                                    username text NOT NULL,
                                    gender text NOT NULL,
                                    age integer NOT NULL,
                                    language text NOT NULL,
                                    city text NOT NULL,
                                    education integer NOT NULL,
                                    specialization integer NOT NULL
                                    );
                            '''

    sql_create_questions1 = ''' CREATE TABLE IF NOT EXISTS db1 (
                                    id integer REFERENCES db0(id) ON DELETE CASCADE ON UPDATE NO ACTION,
                                    city text NOT NULL,
                                    river text NOT NULL,
                                    countryside text NOT NULL,
                                    lake text NOT NULL,
                                    island text NOT NULL,
                                    state text NOT NULL,
                                    mountain text NOT NULL,
                                    peninsula text NOT NULL,
                                    sierra text NOT NULL,
                                    square text NOT NULL
                                    );
                            '''

    sql_create_questions2 = ''' CREATE TABLE IF NOT EXISTS db2 (
                                    id integer REFERENCES db0(id) ON DELETE CASCADE ON UPDATE NO ACTION,
                                    city text NOT NULL,
                                    river text NOT NULL,
                                    countryside text NOT NULL,
                                    lake text NOT NULL,
                                    island text NOT NULL,
                                    state text NOT NULL,
                                    mountain text NOT NULL,
                                    peninsula text NOT NULL,
                                    sierra text NOT NULL,
                                    square text NOT NULL
                                    );
                            '''

    sql_create_search = ''' CREATE TABLE IF NOT EXISTS db3 (
                                    phrase text NOT NULL,
                                    gender text NOT NULL,
                                    lage integer NOT NULL,
                                    rage integer NOT NULL,
                                    education text NOT NULL,
                                    specialization text NOT NULL
                                    );
                        '''
    
    conn = create_connection(DATABASE)
    if conn is not None:
        create_table(conn, sql_create_questions0)
        create_table(conn, sql_create_questions1)
        create_table(conn, sql_create_questions2)
        create_table(conn, sql_create_search)
        conn.commit()
    else:
        print('Can\'t create the database connection')
    
    app.run(host='0.0.0.0') # на локальном компьютере: вводить localhost:5000 или 0.0.0.0:5000
