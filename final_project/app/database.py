"""Defines all the functions related to the database"""
from app import db
from flask import render_template
from app import app
from webforms import SearchForm

def fetch_games() -> dict:
    # Read all tasks listed in the todo table
    # Returns: a list of dictionaries
    conn = db.connect()
    query_results = conn.execute("Select * from Game;").fetchall()
    conn.close()
    game_list = []
    for ret in query_results:
        item = {
            "gameId": ret[0],
            "name": ret[1],
            "year": ret[2],
            "genre": ret[3],
        }
        game_list.append(item)
    return game_list

@app.route('/search', methods=["POST"])
def search():
        form = SearchForm()
        data = form.searched.data
        conn = db.connect()
        print('SELECT * FROM Game WHERE name like "%{}%";'.format(data))
        query = conn.execute('SELECT * FROM Game WHERE name like "{}";'.format(data))
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
