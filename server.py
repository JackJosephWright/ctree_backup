from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from random import sample, randint
import pandas as pd
import werkzeug


def get_LA():
    a = db.session.query(Last_Accessed).filter(Last_Accessed.id==1).first()
    p1 = a.pic_one
    p2 = a.pic_two
    #a.pic_one = index_list[0]
    #a.pic_two = index_list[1]
    #db.session.commit()
    return ([p1,p2])
def new_random(index_list):
    a = db.session.query(Last_Accessed).filter(Last_Accessed.id==1).first()
    a.pic_one = index_list[0]
    a.pic_two = index_list[1]
    db.session.commit()
def set_winner(win, p1,p2):
    if request.form['complex']=='TRUE':
            winner = p1
            loser = p2
    else:
            winner = p2
            loser = p1
    return ([winner,loser])
def commit_winner(winner, loser):
    winner_query = db.session.query(Grades).filter(Grades.pic_number == winner).first()
    print(winner_query.W)
    winner_query.W +=1
    print(winner_query.W)
    db.session.commit()
    winner_query_check = db.session.query(Grades).filter(Grades.pic_number == winner).first()
    print(winner_query_check.W)
    loser_query = db.session.query(Grades).filter(Grades.pic_number ==loser).first()
    loser_query.L +=1
    db.session.commit()
app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:password@localhost:5432/compare_tree'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgres://irbfaicngxcfud:503c504e8bd4ecc7364fdf57fe13b8dd299ad9f2e19a48a080d9c0406faa5cf2@ec2-184-73-243-101.compute-1.amazonaws.com:5432/d1e7gf83mnobjj'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True, echo=False)
#set to query database

class Grades(db.Model):
    __tablename__ = 'scores_table'
    pic_number = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(200))
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)

    def __init__(self, pic_number, link, W, L):
        self.pic_number = pic_number
        self.link = link
        self.W = W
        self.L = L
class Last_Accessed(db.Model):
    __tablename__='last_accessed'
    id = db.Column(db.Integer, primary_key = True)
    pic_one = db.Column(db.Integer)
    pic_two = db.Column(db.Integer)
    
    def __init__(self, pic_one, pic_two):
        self.pic_one = pic_one
        self.pic_two = pic_two

  
@app.route('/', methods = ['GET','POST'])
def index():


    
    
    full_link_list=['static/images/ss0.png','static/images/ss1.png','static/images/ss2.png','static/images/ss3.png','static/images/ss4.png','static/images/ss5.png','static/images/ss6.png','static/images/ss7.png','static/images/ss8.png','static/images/ss9.png','static/images/ss10.png','static/images/ss11.png','static/images/ss12.png','static/images/ss13.png','static/images/ss14.png','static/images/ss15.png','static/images/ss16.png','static/images/ss17.png','static/images/ss18.png','static/images/ss19.png','static/images/ss20.png','static/images/ss21.png']
    if request.method == 'GET':
        
        index_list = sample(range(0,22),2)
        
        new_random(index_list)
        
        
        link_list = list(map(full_link_list.__getitem__,index_list))
        
    else:
        
        
        
        p1, p2 = get_LA()
            
        winner, loser = set_winner(request.form['complex'], p1,p2)
            
        commit_winner(winner, loser)

        index_list = sample(range(0,22),2)
            
        new_random(index_list)
            
        link_list = list(map(full_link_list.__getitem__,index_list))
            
        
    return render_template('index.html', images = index_list, img_list = link_list)
@app.route('/submit_db', methods = ['GET'])
def submit():
    a = db.session.query(Grades).all()
    df = pd.DataFrame(columns = ['pic_number','link','W','L'])
    
    for rating in db.session.query(Grades).all():
        row = [rating.pic_number,rating.link,rating.W,rating.L]
        df.loc[rating.pic_number] = row
    t =pd.DataFrame(df[['pic_number','link','W','L']]).set_index('pic_number')
    t['win_metric'] = t['W']/(t['W']+t['L']+.01)
    t = t.sort_values(by=['win_metric'],ascending=False).to_html(classes='data')
    t_list = [t]
    return render_template('results.html', tables = t_list)

if __name__ =='__main__':
    app.run()