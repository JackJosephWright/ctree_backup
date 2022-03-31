
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
class Raw(db.Model):
    __tablename__ = 'raw_data'
    id = db.Column(db.Integer, primary_key = True)
    W = db.Column(db.String(200))
    L = db.Column(db.String(200))
    def __init__(self, W,L):
        self.W = W
        self.L = L