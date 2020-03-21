from flask import Flask
from flask import render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)


app = Flask(__name__)
app.config['SECRET_KEY'] ='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
db = SQLAlchemy(app)

class ksouravong_apps(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    category_rank = db.Column(db.Integer)
    app_type = db.Column(db.String(10))
    total_ratings = db.Column(db.Integer)

    def __repr__(self):
        return "ID: {0} | App Name: {1} | Category: {2} | Category Rank: {3} | Free or Paid: {4} | Total Ratings: {5}".format(self.app_id, self.app_name, self.category, self.category_rank, self.app_type, self.total_ratings)

class MobileAppForm(FlaskForm):
    app_name = StringField('App Name:', validators=[DataRequired()])
    category = StringField('Category:', validators=[DataRequired()])
    category_rank = StringField('Category Ranking:', validators=[DataRequired()])
    app_type = StringField('Free or Paid:', validators=[DataRequired()])
    total_ratings = StringField('Total Ratings:', validators=[DataRequired()])

@app.route('/')
def index():
    all_apps = ksouravong_apps.query.all()
    return render_template('index.html', apps=all_apps, pageTitle='Mobile Apps')

@app.route('/add_app', methods=['GET', 'POST'])
def add_app():
    form = MobileAppForm()
    if form.validate_on_submit():
        app = ksouravong_apps(app_name=form.app_name.data, category=form.category.data, category_rank=form.category_rank.data, app_type=form.app_type.data, total_ratings=form.total_ratings.data)
        db.session.add(app)
        db.session.commit()
        return redirect('/')

    return render_template('add_app.html', form=form, pageTitle='Add New App')

if __name__ == '__main__':
    app.run(debug=True)
