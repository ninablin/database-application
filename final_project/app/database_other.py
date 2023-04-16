"""Defines all the functions related to the database"""
from app import db
from flask import render_template
from app import app
from webforms import SearchForm

#IN PROGRESS
import random
item_idx = [0]

def get_name():
    return random.choice(["Ann", "Bob", "Chris", "Daniel"])


def fetch_games() -> dict:
    # Read all tasks listed in the todo table
    # Returns: a list of dictionaries
    conn = db.connect()
    query_results = conn.execute("Select * from Game;").fetchall()
    conn.close()
    game_list = []
    for result in query_results:
        item = {
            "gameId": result[0],
            "name": result[1],
            "year": result[2],
            "genre": result[3]
        }
        game_list.append(item)
    return game_list


def fetch_game_info() -> dict:
    # Read all tasks listed in the todo table
    # Returns: a list of dictionaries
    conn = db.connect()
    query_results = conn.execute("Select * from Game_info;").fetchall()
    conn.close()
    item_list = []
    for result in query_results:
        item = {
            "gameId": result[0],
            "review": result[1],
            "summary": result[2],
            "platform": result[3],
            "publisher": result[4]
        }
        item_list.append(item)
        # print(game_list)
    return item_list


def fetch_item_list() -> dict:
    # Read all tasks listed in the todo table
    # Returns: a list of dictionaries
    conn = db.connect()
    query_results = conn.execute("Select * from Item_list;").fetchall()
    conn.close()
    game_list = []
    for result in query_results:
        item = {
            "itemId": result[0],
            "listId": result[1],
            "note": result[2],
            "gameId": result[3],
            "userId": result[4],
            "color": result[5]
        }
        game_list.append(item)
        # print(game_list)
    return game_list


def update_game(gameId, target, text) -> dict:
    conn = db.connect()
    if target == 'name':
        query = 'Update Game set name = "{}" where gameId = {};'.format(text, gameId)
    elif target == 'year':
        query = 'Update Game set year = "{}" where gameId = {};'.format(text, gameId)
    else:
        query = 'Update Game set genre = "{}" where gameId = {};'.format(text, gameId)
    conn.execute(query)
    conn.close()


def update_game_info(gameId, target, text) -> dict:
    conn = db.connect()
    if target == 'review':
        query = 'Update Game_info set review = "{}" where gameId = {};'.format(text, gameId)
    if target == 'summary':
        query = 'Update Game_info set summary = "{}" where gameId = {};'.format(text, gameId)
    if target == 'platform':
        query = 'Update Game_info set platform = "{}" where gameId = {};'.format(text, gameId)
    else:
        query = 'Update Game_info set publisher = "{}" where gameId = {};'.format(text, gameId)
    conn.execute(query)
    conn.close()


def insert_new_game(listId, note, gameId):
    global item_idx
    item_idx[0] += 1
    print(item_idx[0])
    conn = db.connect()
    # print("asdawda")
    query = 'Insert INTO Item_list (itemId, listId, note, gameId, userId, color) VALUES ({}, {}, "{}", {}, "{}", "{}")'.format(item_idx[0], listId, note, gameId, "1", "Black")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    conn.close()


def delete_item_list(itemId):
    global item_idx
    conn = db.connect()
    query = 'Delete From Item_list where itemId = {};'.format(itemId)
    conn.execute(query)
    conn.close()
    item_idx[0] -= 1
    print(item_idx[0])




# def update_list_info(gameId, target, text) -> dict:
def update_list_info(itemId, newNote):
    conn = db.connect()
    # query = 'Update Game_info set publisher = "{}" where gameId = {};'.format(text, gameId)
    query = 'Update Item_list set note = "{}" where itemId = {};'.format(newNote, itemId)
    conn.execute(query)
    conn.close()


# search from game table 
def searchItemCategory(targetName):
    conn = db.connect()
    # query = conn.execute('SELECT * FROM Game WHERE CONTAINS (Game.name, "{}");'.format(targetName))
    # search = "%" + targetName + "%"
    # print(search)
    print('SELECT * FROM Game WHERE name like "%{}%";'.format(targetName))
    query = conn.execute('SELECT * FROM Game WHERE name like "{}";'.format(targetName))
    conn.close()
    query_result = [x for x in query]
    targetItem = []
    # print(targetItem)
    for ret in query_result:
        item = {
            "gameId": ret[0],
            "name": ret[1],
            "year": ret[2],
            "genre": ret[3]
        }
    targetItem.append(item)
    return targetItem

def get_game_info(gameId):
    conn = db.connect()
    query = 'Select name, genre, review From Game Left Join Game_info Using (gameId) Where gameId = {};'.format(gameId)
    results = conn.execute(query).fetchall()
    conn.close()
    game_info= []
    for result in results:
        item = {
            "name": result[0],
            "genre": result[1],
            "review": result[2],
        }
        game_info.append(item)
        # print(game_info)
    return game_info

# Advanced query 1: Show popular games in NA on Playstation platform
# Input: None
# Output: sales, game name and review score for popular games sold on the PlayStation platform
def advancedQuery1():
    conn = db.connect()
    query = conn.execute('SELECT Game.name, Game_info.review, popularGames.Sale_NA FROM Game NATURAL JOIN Game_info JOIN (SELECT gameId, Sale_NA FROM Sales WHERE Sale_NA > 2) AS popularGames WHERE platform = "PlayStation 3" AND Game.gameId = popularGames.gameId ORDER BY popularGames.Sale_NA DESC, Game.name;').fetchall()
    conn.close()
    popularGames = []
    for result in query:
        item = {
            "name": result[0],
            "review": result[1],
            "Sale_NA": result[2]
        }
        popularGames.append(item)
    return popularGames


# Advanced query 2:
# Input: None
# Output: 
def advancedQuery2():
    conn = db.connect()
    query = conn.execute('SELECT gameId, name, AVG(review) as average_review FROM Game LEFT JOIN Game_info USING(gameId) LEFT JOIN Sales USING(gameId) WHERE platform = "PC" AND summary like "T" AND Sale_EU > 1 OR year IN (SELECT year FROM Game WHERE name LIKE "2") GROUP BY gameId HAVING average_review > 4 ORDER BY gameId LIMIT 15').fetchall()
    conn.close()
    results = []
    for result in query:
        item = {
            "gameId": result[0],
            "name": result[1],
            "average_review": result[2]
        }
        results.append(result)
    return results


def getRank():
    conn = db.connect()
    query = conn.execute('Select name, genre, platform, review From Game Left Join Game_info USING(gameId) Left join Sales USING(gameId) Order By Sale_Global DESC LIMIT 50').fetchall()
    conn.close()
    result = []
    for res in query:
        item = {
            "name": res[0],
            "genre": res[1],
            "platform": res[2],
            "review": res[3]
        }
        # print(item)
        result.append(item)
    return result

@app.route('/search', methods=["POST"])
def search():
        form = SearchForm()
        data = form.searched.data
        conn = db.connect()
        print('SELECT * FROM Game WHERE name like "%{}%";'.format(data))
        query = conn.execute('SELECT * FROM Game WHERE name like "%%{}%%";'.format(data))
        conn.close()
        query_result = [x for x in query]
        targetItem = []
        for ret in query_result:
            item = {
                "gameId": ret[0],
                "name": ret[1],
                "year": ret[2],
                "genre": ret[3]
            }
            targetItem.append(item)
        return render_template("search.html", 
                form=form,
                targetItem=targetItem)


@app.route('/display')
def display():
    conn = db.connect()
    query = conn.execute('SELECT Game.name, Game_info.review, popularGames.Sale_NA FROM Game NATURAL JOIN Game_info JOIN (SELECT gameId, Sale_NA FROM Sales WHERE Sale_NA > 2) AS popularGames WHERE platform = "PlayStation 3" AND Game.gameId = popularGames.gameId ORDER BY popularGames.Sale_NA DESC, Game.name;').fetchall()
    conn.close()
    popularGames = []
    for result in query:
        item = {
            "name": result[0],
            "review": result[1],
            "Sale_NA": result[2]
        }
        popularGames.append(item)
    return render_template("display.html", 
                targetItem=popularGames)


@app.route('/advanced2')
def advanced2():
    conn = db.connect()
    query = conn.execute('SELECT gameId, name, year, AVG(review) as average_review FROM Game LEFT JOIN Game_info USING(gameId) LEFT JOIN Sales USING(gameId) WHERE platform = "PC" AND summary like "T" AND Sale_EU > 1 OR year IN (SELECT year FROM Game WHERE name LIKE "2%%") GROUP BY gameId HAVING average_review > 4 ORDER BY gameId LIMIT 15').fetchall()
    conn.close()
    results = []
    for result in query:
        item = {
            "gameId": result[0],
            "name": result[1],
            "year": result[2],
            "average_review": result[3]
        }
        results.append(item)
    return render_template("advanced2.html", 
                targetItem=results)


def fetch_final_table():
    # Read all games listed in the final table executed by the stored procedure
    # Returns: 
    conn = db.connect()
    query_results = conn.execute("Select * from FinalTable Order by newScore desc").fetchall()
    conn.close()
    game_list = []
    for result in query_results:
        item = {
            "gameId": result[0],
            "newScore": result[1],
            "newTag": result[2],
            "gameName": result[3]
        }
        # gameId = item['gameId']
        # game_info = get_game_info(gameId)
        # item.update(game_info[0])
        game_list.append(item)
        # print(item)
    return game_list

def fetch_final_table2():
    # Read all games listed in the final table executed by the stored procedure
    # Returns: 
    conn = db.connect()
    query_results = conn.execute("Select * from FinalTable2 Order by newGlobalSale desc").fetchall()
    conn.close()
    game_list = []
    for result in query_results:
        item = {
            "gameName": result[0],
            "totalSale": result[1],
            "newTag": result[2]
        }
        game_list.append(item)
    return game_list


