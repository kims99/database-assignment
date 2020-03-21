from flask import Flask
from flask import render_template, redirect, request, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
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
    app_id = IntegerField('App ID:')
    app_name = StringField('App Name:', validators=[DataRequired()])
    category = StringField('Category:', validators=[DataRequired()])
    category_rank = IntegerField('Category Ranking:', validators=[DataRequired()])
    app_type = StringField('Free or Paid:', validators=[DataRequired()])
    total_ratings = IntegerField('Total Ratings:', validators=[DataRequired()])

@app.route('/')
def index():
    all_apps = ksouravong_apps.query.all()
    return render_template('index.html', apps=all_apps, pageTitle='Mobile Apps')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        print('post method')
        form = request.form
        search_value = form['search_string']
        search = "%{0}%".format(search_value)
        results = ksouravong_apps.query.filter(or_(ksouravong_apps.app_name.like(search),
                                                ksouravong_apps.category.like(search))).all()
        return render_template('index.html', apps=results, pageTitle='Mobile Apps', legend="Search Results")
    else:
        return redirect("/")


@app.route('/add_app', methods=['GET', 'POST'])
def add_app():
    form = MobileAppForm()
    if form.validate_on_submit():
        app = ksouravong_apps(app_name=form.app_name.data, category=form.category.data, category_rank=form.category_rank.data, app_type=form.app_type.data, total_ratings=form.total_ratings.data)
        db.session.add(app)
        db.session.commit()
        return redirect('/')

    return render_template('add_app.html', form=form, pageTitle='Add New App')


@app.route('/delete_app/<int:app_id>', methods=['GET', 'POST'])
def delete_app(app_id):
    if request.method == 'POST':
        app = ksouravong_apps.query.get_or_404(app_id)
        db.session.delete(app)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/")


@app.route('/app/<int:app_id>', methods=['GET', 'POST'])
def get_app(app_id):
    app = ksouravong_apps.query.get_or_404(app_id)
    return render_template('app.html', form=app, pageTitle='App Details', legend="App Details")


@app.route('/app/<int:app_id>/update', methods=['GET', 'POST'])
def update_app(app_id):
    app = ksouravong_apps.query.get_or_404(app_id)
    form = MobileAppForm()

    if form.validate_on_submit():
        app.app_name = form.app_name.data
        app.category = form.category.data
        app.category_rank = form.category_rank.data
        app.app_type = form.app_type.data
        app.total_ratings = form.total_ratings.data
        db.session.commit()
        return redirect(url_for('get_app', app_id=app.app_id))
   
    form.app_id.data = app.app_id
    form.app_name.data = app.app_name 
    form.category.data = app.category  
    form.category_rank.data = app.category_rank  
    form.app_type.data = app.app_type 
    form.total_ratings.data = app.total_ratings
    return render_template('update_app.html', form=form, pageTitle='Update App', legend="Update An App")




if __name__ == '__main__':
    app.run(debug=True)
