from app import app
from flask import render_template, request, jsonify
from app import database_other as db_helper

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title='Game Center')

@app.route("/account")
def account():
    return render_template("account.html", title='Game Center')

@app.route("/login")
def login():
    return render_template("login.html", title='Game Center')

@app.route("/signup")
def signup():
    return render_template("signup.html", title='Game Center')

@app.route("/rank")
def rank():
    items = db_helper.fetch_final_table()
    return render_template("rank.html", title='Game Center', items=items)

@app.route("/rank2")
def rank2():
    items = db_helper.fetch_final_table2()
    return render_template("rank_by_sale.html", title='Game Center', items=items)

@app.route("/category")
def category():
    return render_template("category.html", title='Game Center')


@app.route("/lists")
def lists():
    items = db_helper.fetch_item_list()
    # print(items)
    for i in range(len(items)):
        item = items[i]
        gameId = item['gameId']
        game_info = db_helper.get_game_info(gameId)
        # print(game_info)
        item.update(game_info[0])
        # print(item)
        items[i] = item
    return render_template("lists.html", title='Game Center', items=items)


@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    gameId = data['note']
    db_helper.insert_new_game(1, "", gameId)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/edit/<int:itemId>", methods=['POST'])
def update(itemId):
    """ recieved post requests for entry updates """
    data = request.get_json()
    newNote = data['note']
    db_helper.update_list_info(itemId, newNote)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/delete/<int:itemId>", methods=['POST'])
def delete(itemId):
    try:
        # print("aaaaaa")
        # data = request.get_json()
        # item_id = data['itemId']
        db_helper.delete_item_list(itemId)
        result = {'success': True, 'response': 'Removed Task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}
    return jsonify(result)
