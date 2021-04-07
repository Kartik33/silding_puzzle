"""Python Flask WebApp Auth0 integration example
"""
from functools import wraps
from os import environ as env


from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask import Flask,abort,jsonify,request,redirect, url_for,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import constants
from model.model import db,setup_db,Player,Board
from solve_puzzle import Board as b ,AStarSearch
from model.config import *
from authlib.integrations.flask_client import OAuth
import ast
from auth.auth import requires_auth,AuthError 


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)



AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
DATABASE_URL = env.get(constants.DATABASE_URL)

##########################database connections##############################

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = constants.SECRET_KEY
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = setup_db(app)
migrate = Migrate(app,db)
CORS(app)
##############################################################


##############################Authentication##########################################

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)




@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)




@app.route('/callback')
def callback_handling():
    token = auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    email = userinfo['email']
    name = userinfo['nickname']
    user = Player.query.filter(Player.username==email).one_or_none()
    if not user:
        user = Player(name=name,username=email)
        user.insert()
    return redirect(url_for(
                    '.home',
                    id_token=token['id_token'],
                    access_token=token['access_token'])
                    )
############################################################################################


# Controllers API
@app.route('/')
#@requires_auth()
def home():
    id_token = request.args['id_token']
    jwt = request.args['access_token']
    return jsonify({
                "success":True,
                "jwt":jwt,
                "id_token":id_token
                })


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','*')
    response.headers.add("Access-Control-Allow-Credentials","true")
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,DELETE,OPTIONS')
    return response

#########################Admin##################################

@app.route('/players',methods=['GET'])
@requires_auth(permission=['get:player'])
def getPlayers(payload):
    players = Player.query.all()
    players = [i.only_users() for i in players]
    return jsonify({"success":True,
            "status_code":200,
            "players":players})




@app.route('/player/<int:player_id>',methods=['DELETE'])
@requires_auth(permission=['delete:player'])
def deltePlayer(payload,player_id):
    player = Player.query.filter(Player.id==player_id).one_or_none()
    if not player:
        abort(404)
    player.delete()
    return jsonify({
        "success":True,
        "status_code":200,
        "player_id":player_id
        })

##################################################################


############################Guest Player###########################

@app.route("/guest",methods=["GET"])
def show_board_guest():
    return render_template('home.html')



@app.route("/solve",methods=["GET"])
def geust_solve():
    board = request.args["board"]
    if not board:
        abort(400)
    boardList = [int(i) for i in board.split(",")]
    if len(boardList) != 9 or sorted(boardList) != [i for i in range(9)]:
        abort(400)
    boardObject = b(tuple([int(x) for x in boardList]))
    algorithm = AStarSearch(boardObject)
    result = algorithm.search()
    moves = result['moviments']
    return jsonify({
        "success":True,
        "moves":moves
        })

##############################Player route####################################



@app.route('/player/<int:player_id>/boards', methods=['GET'])
@requires_auth(permission=["get:board"])
def getBoards(payload,player_id):
    username = payload[1]['email'] 
    player = Player.query.filter(Player.username==username).one_or_none()
    if not player:
        abort(404)
    elif player.id != player_id:
        abort(400)
    return jsonify({"success":True,
            "player_id":player_id,
            "player_name":player.name,
            "status_code":200,
            "boards":player.only_boards()})




@app.route('/board/<int:board_id>',methods=['DELETE'])
@requires_auth(permission=["delete:board"])
def deleteBoard(payload,board_id):
    username = payload[1]['email'] 
    player = Player.query.filter(Player.username==username).one_or_none() 
    if not player:
        abort(404)
    boardCol = Board.query\
        .filter(Board.id==board_id)\
        .filter(Board.user_id==player.id)\
        .one_or_none()

    if not boardCol:
        abort(404)
    
    try:
        boardCol.delete()
    except:
        abort(422)
    
    return jsonify({
            "success":True,
            "status_code":200,
            "board_id":board_id})



@app.route('/dummytest',methods=['GET'])
def insertDummy():
    try:
        user1 = Player(id=1,name="kartik",username="kartiktushir@gmial.com")
        user1.insert()
    except Exception as e:
        print(e)
        abort(500)
    try:
        user2 = Player(id=2,name="kunal",username="kunal@gmail.com")
        b1 = Board(id=1,board_state="3892709",moves="aldksfoisdhjfn;osd",user_id=2)
        b2 = Board(id=2,board_state="3892709",moves="aldksfoisdhjfn;osd",user_id=2)
        user2.boards = [b1,b2]
        user2.insert()
    except Exception as e:
        print(e)
        abort(500)

    return jsonify({
        "success":True,
        "status_code":200})



@app.route('/board/<int:board_id>', methods=['PATCH'])
@requires_auth(permission=["update:board"])
def updateBoard(payload,board_id):
    username=payload[1]["email"]
    player = Player.query.filter(Player.username==username).one_or_none()
    if not player:
        abord(404)
    body = request.get_json()
    board = body.get('board',None)
    boardCol = Board.query\
        .filter(Board.id==board_id)\
        .filter(Board.user_id==player.id)\
        .one_or_none()

    if not boardCol:
        abort(400)
    boardList = [int(i) for i in board.split(",")]
    boardObject = b(tuple([int(x) for x in boardList]))
    algorithm = AStarSearch(boardObject)
    result = algorithm.search()
    if result:
        moves = result['moviments']
    else:
        moves = "notpossible"
    try:
        boardCol.moves = str(moves)
        boardCol.board = board
        boardCol.update()
    except:
        abort(422)

    return {
            "success":True,
            "status_code":200,
            "board_id":board_id}





@app.route('/solve',methods=['POST'])
@requires_auth(permission=["post:solve_puzzle"])
def solvePuzzle(payload):
    username = payload[1]['email']
    player = Player.query.filter(Player.username==username).one_or_none() 
    body = request.get_json()
    if not body:
        abort(400)
    board = body.get('board',None)
    if not board or not player:
        abort(400)
    boardList = [int(i) for i in board.split(",")]
    if len(boardList) != 9 or sorted(boardList) != [i for i in range(9)]:
        abort(400)
    boardObject = b(tuple([int(x) for x in boardList]))
    algorithm = AStarSearch(boardObject)
    result = algorithm.search()
    moves = result['moviments']
    try:
        boardColumn = Board(
                      board_state=board,
                      moves=str(moves),
                      user_id=player.id)

        boardColumn.insert()
    except:
        abort(422)

    return jsonify({
        "success":True,
        "status_code":200,
        "user_id":player.id,
        "board_state":board,
        "solution":moves}) 

################################Error Handlers#####################################


@app.errorhandler(400)
def notFound(error):
    return jsonify({
           "success": False, 
           "error": 400,
           "message": "bad request"
           }), 400

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success":False,
        "error":ex.status_code,
        "message":ex.error}),ex.status_code



##############################################################################





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
