from os import environ as env
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask_migrate import Migrate
from flask import Flask


app = Flask(__name__)
db = SQLAlchemy()
def setup_db(app):
    db.app = app
    db.init_app(app)
    return db


class Player(db.Model):

    __tablename__ = 'player'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    username = Column(db.String)
    boards = db.relationship('Board', 
            backref=db.backref('boards',lazy=True),
            cascade="all,delete-orphan")
    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def only_boards(self):
        return [{'board_id':b.id,'board_state':b.board_state}\
                      for b in self.boards]
    
    def only_users(self):
        return {
                "id":self.id,
                "name":self.name,
                "email":self.username
                }



class Board(db.Model):

    __tablename__ = 'board'

    id = Column(db.Integer, primary_key=True)
    board_state = Column(db.String)
    moves = Column(db.String)
    user_id = Column(db.Integer, db.ForeignKey('player.id'), nullable=False)

    def insert(self):
        #self.board_state = ",".join(str(i) for i in self.board)
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()
