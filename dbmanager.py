import sqlite3
import constants



def get_stats(username):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    stats=cursor.execute('SELECT wins, loses, wlratio, rank from users where username='+username)
    stats=stats.fetchall()
    connection.close()
    return stats

def update_stats(username,wins,loses, wlratio,rank):
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET wins='+wins+', loses='+loses+', wlratio='+wlratio+', rank='+rank+' where username='+username)
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
    result = cursor.execute(" SELECT username from users where username="+username)

    if len(result)>0:
        answer=constants.ERROR
    else:
        cursor.execute("INSERT INTO users VALUES("+username+","+password+"0,0,0,0)")
        connection.commit()

    connection.close()
    return answer

def login(username, password):
    answer = constants.ERROR
    connection = sqlite3.connect("serverDB")
    cursor = connection.cursor()
    result = cursor.execute("SELECT username, password from users where username=" + username+" and password="+password)

    if len(result) > 0:
        answer = constants.SUCCESS

    connection.close()
    return answer