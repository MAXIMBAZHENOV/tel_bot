import  sqlite3

sqlite3_connection = sqlite3.connect("tel_db.sqlite")
querry = '''CREATE TABLE spreadsheet1 (user_id INTEGER,message_id INTEGER PRIMARY KEY)'''

cursor = sqlite3_connection.crusor()
cursor.execute(querry)
sqlite3_connection.commit()

querry = '''CREATE TABLE spreadsheet2 (message_id INTEGER PRIMARY KEY, message TEX)'''
cursor = sqlite3_connection.cursor()
cursor.execute(querry)
sqlite3_connection.commit()

cursor.close()
sqlite3_connection.close()