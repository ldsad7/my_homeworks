from flask import Flask, render_template, url_for, request, redirect, session
import json, sqlite3
from sqlite3 import Error

#DATABASE = "C:\\Users\Эдуард\Desktop\myproject\pythonsqlite.sqlite"
DATABASE = "/home/eduard/myproject/pythonsqlite.sqlite"

app = Flask(__name__)

@app.route('/')
def questions0():
    return render_template('questionnaire1.html')

@app.route('/questions1')
def questions1():
    return render_template('questionnaire2.html')

@app.route('/questions2')
def questions2():
    return render_template('questionnaire3.html')

@app.route('/finalpage')
def finalpage():
    return render_template('finalpage.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')  # здесь нужен возврат на страницу поиска
def results():
    
    conn = create_connection(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM db0")
    rows0 = list(cur.fetchall())
    
    cur.execute("SELECT * FROM db1")
    rows1 = list(cur.fetchall())
    
    cur.execute("SELECT * FROM db2")
    rows2 = list(cur.fetchall())
    
    cur.execute("SELECT * FROM db3")
    rows3 = list(cur.fetchall())

    search = list(rows3[-1])

    phrases = search[0].split(', ')
    gend = search[1].split(', ')
    lage = int(search[2])
    rage = int(search[3])
    educ = search[4].split(', ')
    spec = search[5].split(', ')

    num_of_users = 0
    num = 0
    num_of_decl = 0

    for i in range(min(len(rows0), len(rows1), len(rows2))):
        if rows0[i] and rows1[i] and rows2[i]:
            x = rows0[i][3]
            if (rows0[i][2] in gend) and (lage <= x <= rage) and (rows0[i][6] in educ) and (rows0[i][7] in spec):
                num_of_users += 1
                for phrase in phrases:
                    for elem in rows2[i][phrase]:
                        if elem == "1":
                            num_of_decl += 1
                        num += 1
    
    conn.commit()
    return render_template('results.html', value1 = num_of_decl, value2 = num * num_of_users)

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

@app.route('/answers1')
def get_answers1():
    username = request.args['username']
    gender = request.args['gender']
    age = request.args['age']
    language = request.args['language']
    cities = ', '.join(request.args.getlist('city'))
    education = request.args['education']
    specialization = request.args['specialization']

    conn = create_connection(DATABASE)

    with conn:
        db = (username, gender, age, language, cities, education, specialization);
        create_db0(conn, db)
        conn.commit()
    
    return redirect(url_for('questions1'))

@app.route('/answers2')
def get_answers2():
    cities = ', '.join(request.args.getlist('city'))
    rivers = ', '.join(request.args.getlist('river'))
    countrysides = ', '.join(request.args.getlist('countryside'))
    lakes = ', '.join(request.args.getlist('lake'))
    islands = ', '.join(request.args.getlist('island'))
    states = ', '.join(request.args.getlist('state'))
    mountains = ', '.join(request.args.getlist('mountain'))
    peninsula = ', '.join(request.args.getlist('peninsula'))
    sierra = ', '.join(request.args.getlist('sierra'))
    squares = ', '.join(request.args.getlist('square'))
    
    conn = create_connection(DATABASE)

    with conn:
        db = (cities, rivers, countrysides, lakes, islands, states, mountains, peninsula, sierra, squares);
        create_db1(conn, db)
        conn.commit()

    return redirect(url_for('questions2'))
                        
@app.route('/answers3')
def get_answers3():
    cities = ', '.join(request.args.getlist('city'))
    rivers = ', '.join(request.args.getlist('river'))
    countrysides = ', '.join(request.args.getlist('countryside'))
    lakes = ', '.join(request.args.getlist('lake'))
    islands = ', '.join(request.args.getlist('island'))
    states = ', '.join(request.args.getlist('state'))
    mountains = ', '.join(request.args.getlist('mountain'))
    peninsula = ', '.join(request.args.getlist('peninsula'))
    sierra = ', '.join(request.args.getlist('sierra'))
    squares = ', '.join(request.args.getlist('square'))
    
    conn = create_connection(DATABASE)

    with conn:
        db = (cities, rivers, countrysides, lakes, islands, states, mountains, peninsula, sierra, squares);
        db_id = create_db2(conn, db)
        conn.commit()
    
    return redirect(url_for('finalpage'))

@app.route('/answers4', methods=['GET', 'POST'])
def get_answers4():
    phrases = request.args.getlist("phrase")
    if type(phrases) != str:
        phrases = ', '.join(phrases)
    genders = request.args.getlist("gender")
    if type(genders) != str:
        genders = ', '.join(genders)
    lage = int(request.args['lage'])
    rage = int(request.args['rage'])
    education = request.args.getlist("education")
    if type(education) != str:
        education = ', '.join(education)
    specialization = request.args.getlist("specialization")
    if type(specialization) != str:
        specialization = ', '.join(specialization)

    conn = create_connection(DATABASE)

    with conn:
        db = (phrases, genders, lage, rage, education, specialization);
        create_db3(conn, db)
        conn.commit()
    
    return redirect(url_for('results'))

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file) # или здесь лучше заменить на ':memory:'?
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
    sql = ''' INSERT INTO db1(city, river, countryside, lake, island, state, mountain, peninsula, sierra, square)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, db)
    conn.commit()
    return cur.lastrowid

def create_db2(conn, db):
    sql = ''' INSERT INTO db2(city, river, countryside, lake, island, state, mountain, peninsula, sierra, square)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
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
    app.run(host='0.0.0.0')

