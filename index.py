from flask import Flask, render_template, request, url_for,flash
import sqlite3

'''
def connect_db():
    return sqlite3.connect('big_database.db')


def create_tab(restaurant_name):
    conn = connect_db()
    query_cursor = conn.cursor()
    query_cursor.execute('CREATE TABLE ' + restaurant_name + '(id INT PRIMARY KEY AUTOINCREMENT, food TEXT, price DOUBLE, weight INT, tip TEXT)')
    conn.commit()


def insert_in_table(table_name, i_food, i_price, i_weight, i_tip):
    conn = connect_db()
    query_cursor = conn.cursor()
    query_cursor.execute('INSERT INTO ' + table_name  + ' (id,food,price,weight,tip)' + 'VALUES' + '(?,?,?,?)', (i_food, i_price, i_weight, i_tip))
    conn.commit()

'''
app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form_submit.html')


@app.route('/hello/', methods=['POST'])
def hello():
    food = request.form['mancare']
    number = request.form['numar_pers']
    food2 = food.split(',')
    return render_template('form_action_2.html', food=food2, number=number)


@app.route('/inputs', methods=['POST', 'GET'])
def inputs():
    if request.method == 'POST':
        conn = sqlite3.connect('big_database.db')
        curs = conn.cursor()
        rezultat = curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=" + "'" + request.form['restaurant_name'] + "'" + ";")
        if rezultat.fetchone():
            rest_name = request.form['restaurant_name']
            mancare = request.form['food']
            nume_mancare = request.form['food_name']
            greutate = request.form['food_weight']
            pret = request.form['price']
            curs.execute('INSERT INTO ' + rest_name + '(food, price, weight, tip) VALUES(?,?,?,?)', (nume_mancare, pret, greutate, mancare))
            conn.commit()
        else:
            curs.execute('CREATE TABLE ' + request.form['restaurant_name'] + '(id INT PRIMARY KEY, food TEXT, price DOUBLE, weight INT, tip INT)')
            conn.commit()
            rest_name = request.form['restaurant_name']
            mancare = request.form['food']
            nume_mancare = request.form['food_name']
            greutate = request.form['food_weight']
            pret = request.form['price']
            curs.execute('INSERT INTO ' + rest_name + '(food, price, weight, tip) VALUES(?,?,?,?)', (nume_mancare, pret, greutate, mancare))
            conn.commit()
    return render_template('inputs.html')


@app.route('/list', methods=['POST', 'GET'])
def list():
    if request.method == 'POST':
        conn = sqlite3.connect('big_database.db')
        curs = conn.cursor()
        table_name = request.form['table_name']
        if len(table_name):
            rezultat = curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=" + "'" + table_name + "'" + ";")
            if rezultat.fetchone():
                table_value = curs.execute("SELECT * FROM " + table_name)
                value=table_value.fetchall()
                return render_template('list.html',table_result=value,increment=len(value))
        return render_template('list.html', table_name='', increment=0)
    if request.method == 'GET':
        return render_template('list.html', table_name='', increment=0)


if __name__ == '__main__':
    #create_tab("Andone")
    #insert_in_table('Andone', 1, 'ciorba', 50)
    #app.run(host='0.0.0.0', port=8080 ,debug=True)
    app.run(debug=True)
