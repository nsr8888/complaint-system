from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "complaint_secret"


# Database Connection
def get_db():
    return sqlite3.connect("database.db")


# Home (Login)
@app.route('/')
def home():
    return render_template("login.html")


# Register Page
@app.route('/register')
def register():
    return render_template("register.html")


# Register User
@app.route('/register_user', methods=["POST"])
def register_user():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO users(name,email,password,role)
    VALUES (?,?,?,?)
    """, (name, email, password, "student"))

    db.commit()

    return redirect('/')


# Login
@app.route('/login', methods=["POST"])
def login():

    email = request.form['email']
    password = request.form['password']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    SELECT * FROM users
    WHERE email=? AND password=?
    """, (email, password))

    user = cur.fetchone()

    if user:

        session['user_id'] = user[0]
        session['role'] = user[4]

        if user[4] == "admin":
            return redirect('/admin')
        else:
            return redirect('/dashboard')

    return "Invalid Login"


# Student Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    SELECT * FROM complaints
    WHERE user_id=?
    """, (session['user_id'],))

    data = cur.fetchall()

    return render_template("dashboard.html", data=data)


# Add Complaint
@app.route('/add_complaint', methods=["POST"])
def add_complaint():

    subject = request.form['subject']
    message = request.form['message']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    INSERT INTO complaints
    VALUES(NULL,?,?,?,?)
    """, (session['user_id'], subject, message, "Pending"))

    db.commit()

    return redirect('/dashboard')


# Admin Panel
@app.route('/admin')
def admin():

    if 'role' not in session or session['role'] != "admin":
        return redirect('/')

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    SELECT complaints.id,
           users.name,
           complaints.subject,
           complaints.message,
           complaints.status
    FROM complaints
    JOIN users ON complaints.user_id = users.id
    """)

    data = cur.fetchall()

    return render_template("admin.html", data=data)


# Update Status
@app.route('/update/<id>/<status>')
def update(id, status):

    db = get_db()
    cur = db.cursor()

    cur.execute("""
    UPDATE complaints
    SET status=?
    WHERE id=?
    """, (status, id))

    db.commit()

    return redirect('/admin')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Run App
if __name__ == "__main__":
    app.run(debug=True)
