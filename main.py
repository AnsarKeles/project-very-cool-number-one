from flask import Flask, request, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'veryhardpasswordfr'

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            avatar TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user[0]  # сохранили ID в сессию
            return redirect('/profile')
        else:
            return 'Неверный логин или пароль!'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        avatar = request.form.get('avatar')
        username = request.form.get('login')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        weak_passwords = [
            "123456", "password", "123456789", "12345", "12345678",
            "qwerty", "abc123", "football", "monkey", "letmein",
            "111111", "1234", "1234567", "dragon", "baseball",
            "sunshine", "iloveyou", "trustno1", "princess", "admin",
            "welcome", "password1", "123123", "flower", "password123"
        ]

        if len(username) < 4 or len(username) > 20:
            return 'Длинна вашего username должна быть больше 4 и меньше 20'
        if len(password) < 8 or password in weak_passwords:
            return 'Пароль слишком короткий или слишком простой'
        if password != confirm_password:
            return 'Пароли не совпадают!'
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()

        if existing_user:
            conn.close()
            return 'Пользователь с таким именем уже существует!'
        c.execute('INSERT INTO users (avatar, username, password) VALUES (?, ?, ?)', (avatar, username, password))
        conn.commit()
        conn.close()
        session['user_id'] = c.lastrowid
        return redirect('/profile')
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT avatar, username FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()

    if not user:
        return redirect('/login')

    avatar_url, username = user

    return render_template('profile.html', avatar=avatar_url, username=username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

#fldkg;fdkg;ldf