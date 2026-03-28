
from flask import Flask, session, redirect, url_for,render_template,request,flash
from database import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Your_secret_key_here'



@app.route('/register/', methods=['GET', "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form.get('password')
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('register'))
        if not any(num in '1234567890' for num in password):
            flash('Password must have at least one number')
            return redirect(url_for('register'))

        user = get_user(username)
        if user:
            return redirect(url_for('register'))
        hashedp = generate_password_hash(password)
        add_user(username,hashedp)
        flash('Successfully registered')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        if user and check_password_hash(user['password'],password):
            session['user_id'] = user['id']
            flash('Successfully logged in')
            return redirect(url_for('home'))        
    return render_template('login.html')



@app.route('/home/', methods=['GET', "POST"])
def home():
    if session.get('user_id'):
        conn = get_db_connection()
        user_id = session.get('user_id')
        if request.method == 'POST':
            content = request.form.get('content')
            if content:
                add_note(user_id, content)
                return redirect(url_for('home'))
        notes = get_notes(user_id,)
        conn.close()
        return render_template('home.html',notes=notes)
    return redirect(url_for('login'))



@app.route('/notes_deletion/<int:note_id>', methods=['GET','POST'])
def delete_notes(note_id):
    if session.get('user_id'):
        user_id = session.get('user_id')
        delete_note(note_id,user_id)
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/edit_note/<int:note_id>',methods = ['GET','POST'])
def edit_note(note_id):
    if session.get('user_id'):
        user_id = session.get('user_id')
        if request.method == 'POST':
            new_content = request.form.get('content')
            upd_note(note_id,user_id,new_content)
            return redirect(url_for('home'))


@app.route('/profile/', methods=['GET','POST'])
def profile():
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = user_by_id(user_id)
        notes = get_notes(user_id)
        notes_num = len(notes)
        if request.method == 'POST':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            if not check_password_hash(user['password'], old_password):
                flash('Old password is incorrect')
                return redirect(url_for('profile'))
            if len(new_password) < 8:
                flash('Password must be at least 8 characters long')
                return redirect(url_for('profile'))
            if not any(num in '1234567890' for num in new_password):
                flash('Password must have at least one number')
                return redirect(url_for('profile'))
            upd_password(user_id, generate_password_hash(new_password))
            flash('Password successfully changed')
            return redirect(url_for('profile'))
        return render_template('profile.html', user=user, notes=notes, notes_num=notes_num)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)


