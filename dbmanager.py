import sqlite3
from constants import *


def get_stats(username):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    stats=cursor.execute('SELECT wins, loses, wlratio, rank from users where username=?',(username,))
    stats=" ".join(str(stats.fetchone()).split(","))[SECOND:LAST]
    connection.close()
    return stats

def update_stats(username,wins,loses, wlratio,rank):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET wins=?, loses=?, wlratio=?, rank=? where username=?',(wins,loses,wlratio,rank,username))
    connection.commit()
    connection.close()

def change_stats_after_game(username, won_game):
    current_stats=get_stats(username)
    wins, loses, wlratio, rank=current_stats.split("  ")
    wins, loses, wlratio, rank=int(wins), int(loses), float(wlratio), int(rank)
    if won_game:
        rank+=SCORE_TO_ADD_AFTER_WIN
        wins+=1
    else:
        if rank>=MINIMUM_RANK_TO_SUBTRACT_SCORE_FROM:
            rank-=SCORE_TO_SUBTRACT_AFTER_LOSS
        loses+=1

    wlratio=round(wins/(wins+loses)*100,2)
    update_stats(username,wins,loses,wlratio,rank)



def create_table_if_does_not_exist():
    connection = sqlite3.connect("serverDB")
    cursor=connection.cursor()
    cursor.execute('CREATE TABLE users (username text, password text, wins int, loses int, wlratio float, rank int)')
    connection.commit()
    connection.close()

def register(username, password):
    answer=SUCCESS
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    result = cursor.execute(" SELECT username from users where username=?",(username,))
    result=result.fetchall()

    if len(result)>0:
        answer=ERROR
    else:
        cursor.execute("INSERT INTO users VALUES(?,?,0,0,0,0)",(username,password))
        connection.commit()

    connection.close()
    return answer

def login(username, password):
    answer = ERROR
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    result = cursor.execute("SELECT username, password from users where username=? and password=?",(username,password))
    result=result.fetchall()

    if len(result) > 0:
        answer = SUCCESS

    connection.close()
    return answer