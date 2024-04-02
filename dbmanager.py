import sqlite3
import constants



def get_stats(username):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    stats=cursor.execute('SELECT wins, loses, wlratio, rank from users where username=?',(username,))
    stats=" ".join(str(stats.fetchone()).split(","))[1:-1]
    connection.close()
    return stats

def update_stats(username,wins,loses, wlratio,rank):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET wins=?, loses=?, wlratio=?, rank=? where username=?',(wins,loses,wlratio,rank,username))
    connection.commit()
    connection.close()

def create_table_if_does_not_exist():
    connection = sqlite3.connect("serverDB")
    cursor=connection.cursor()
    cursor.execute('CREATE TABLE users (username text, password text, wins int, loses int, wlratio float, rank int)')
    connection.commit()
    connection.close()

def register(username, password):
    answer=constants.SUCCESS
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    result = cursor.execute(" SELECT username from users where username=?",(username,))
    result=result.fetchall()

    if len(result)>0:
        answer=constants.ERROR
    else:
        cursor.execute("INSERT INTO users VALUES(?,?,0,0,0,0)",(username,password))
        connection.commit()

    connection.close()
    return answer

def login(username, password):
    answer = constants.ERROR
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    result = cursor.execute("SELECT username, password from users where username=? and password=?",(username,password))
    result=result.fetchall()

    if len(result) > 0:
        answer = constants.SUCCESS

    connection.close()
    return answer