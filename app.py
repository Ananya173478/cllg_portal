from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 course TEXT,
                 email TEXT)''')
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        email = request.form['email']

        conn = sqlite3.connect('students.db')
        conn.execute("INSERT INTO students (name, course, email) VALUES (?, ?, ?)",
                     (name, course, email))
        conn.commit()
        conn.close()
        return redirect('/view')

    return render_template('add.html')

@app.route('/view')
def view_students():
    conn = sqlite3.connect('students.db')
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('view.html', students=students)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
