import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from flask import Flask
import config

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    dp.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    user = User(
        name='Kartik',
        username='Kartik33',
        phone='6624970195',
        address='25 Dawg Dr',
        age=27,
        board_id=0
    )

    board = Board(
        board_state = "123456789",
        moves = "[(1,1),(2,2),(3,3)]",
        user_id = 1
    )


class User(db.Model):

    __tablename__ = 'user'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    username = Column(db.String)
    phone = Column(db.String)
    address = Column(db.String)
    age = Column(db.Integer)
    boards = db.relationship('Board', 
            backref=db.backref('boards',lazy=True),
            cascade="all,delete-orphan")
    

    def only_boards(self):
        return {
            "id":self.id,
            "name":self.name,
            "boards":[{'board_id':b.id,'board_state':b.board_state}\
                      for b in self.boards]
        }



class Board(db.Model):

    __tablename__ = 'board'

    id = Column(db.Integer, primary_key=True)
    board_state = Column(db.String)
    moves = Column(db.String)
    user_id = Column(db.Integer, db.ForeignKey('User.id'), nullable=False)


    def moves(self):
        return {
            "id":self.id,
            "moves":self.moves
        }




#class Permission(db.Model):
#
#    __tablename__ = 'permission'
#
#    id = db.Column(db.Integer, primary_key=True)
#    permission = db.Column(db.String)
#    role_id = db.Column(db.Integer)
#
#
#class Role(db.Model):
#    
#    __tablename_- = 'role'
#    id = db.Column(db.Integer, primary_key=True)
#    role = db.Column(db.String)
