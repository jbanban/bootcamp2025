from flask import Flask, render_template, redirect, session, url_for, request, flash, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 16 * 1024 * 1024

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wowixczzzzz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activityOne.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

db = SQLAlchemy(app)

class Base(DeclarativeBase):
    pass

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(50))
    birthdate: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(100))
    image: Mapped[str] = mapped_column(String(200), nullable=True)  # Allow null

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/reg', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        bdate = request.form['bdate']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'error')
            return render_template('register.html')

        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)
                image_filename = filename

        hashed_password = generate_password_hash(password)
        new_user = User(
            image=image_filename,
            name=name,
            birthdate=bdate,
            address=address,
            username=username,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    current_user = User.query.get(user_id)

    image_url = None
    if current_user and current_user.image:
        image_path = os.path.join(app.static_folder, 'img', current_user.image)
        if os.path.exists(image_path):
            image_url = url_for('static', filename=f'img/{current_user.image}')
        else:
            flash('Image file not found on server.', 'warning')

    return render_template('home.html', image_url=image_url, user=current_user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
