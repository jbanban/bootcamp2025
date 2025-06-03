from flask import Flask, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wowixczzzzz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activityOne.db'
db = SQLAlchemy(app)

Class Base(DeclarativeBase):
    pass

Class User(db.model):
    __tablename__ = "user"

app.route('/')
def login():
    return redirect (url_for('home'))


app.route('/reg')
def register():
    return redirect (url_for('login'))

app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=False)