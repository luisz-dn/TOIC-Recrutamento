from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)

DB_FILE = "membros.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS membros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_game TEXT,
                numero TEXT,
                local TEXT,
                recrutador TEXT
            )
        """)
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM membros')
    membros = c.fetchall()
    conn.close()
    return render_template('index.html', membros=membros)

@app.route('/add', methods=['POST'])
def add():
    nome_game = request.form['nome_game']
    numero = request.form['numero']
    local = request.form['local']
    recrutador = request.form['recrutador']

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO membros (nome_game, numero, local, recrutador) VALUES (?, ?, ?, ?)',
              (nome_game, numero, local, recrutador))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM membros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    nome_game = request.form['nome_game']
    numero = request.form['numero']
    local = request.form['local']
    recrutador = request.form['recrutador']

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE membros SET nome_game=?, numero=?, local=?, recrutador=? WHERE id=?",
              (nome_game, numero, local, recrutador, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=81)
