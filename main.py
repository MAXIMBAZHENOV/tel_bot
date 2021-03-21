import telebot
import sqlite3

bot = telebot.TeleBot('your token')

def add_msg(message):
    sql_connection = sqlite3.connect("tel_db.sqlite")
    cursor = sql_connection.cursor()
    user_id = message.from_user.id
    query_check = cursor.execute('''SELECT * FROM spreadsheet WHERE user_id = ?''', (user_id,)).fetchone()
    if(query_check is None):
        message_id = message.from_user.id * 10 + 1
        cursor.execute('''INSERT INTO spreadsheet1 (user_id, message_id) VALUES (?, ?)''', (user_id, message_id))
        sql_connection.commit()
        cursor.execute('''INSERT INTO spreadsheet2 (message_id, message) VALUES (?, ?)''', (message_id, record))
        sql_connection.commit()
    else:
        quantity = cursor.execute('''SELECT COUNT(user_id) FROM spreadsheet1 WHERE user_id = ?''', (user_id,)).fetchone()
        message_id = message.from_user.id * 10 + quantity[0] + 1
        cursor.execute('''INSERT INTO spreadsheet1 (user_id, message_id) VALUES (?, ?)''', (user_id, message_id))
        cursor.execute('''INSERT INTO spreadsheet2 (message_id, message) VALUES (?, ?)''', (message_id, record))
        sql_connection.commit()

def show_message(message):
    sql_connection = sqlite3.connect("tel_db.sqlite")
    cursor = sql_connection.cursor()
    user_id = message.from_user.id
    message_id = cursor.execute('''SELECT message_id FROM spreadsheet1 WHERE user_id = ?''', (user_id,)).fetchall()
    result = []
    for i in list(message_id):
        mssg = cursor.execute('''SELECT message FROM spreadsheet2 WHERE message_id = ?''', (i[0],)).fetchone()
        result.append(mssg)
    return result

def delete_message(message, id_message):
    sql_connection = sqlite3.connect("tel_db.sqlite")
    cursor = sql_connection.cursor()
    message_id = message.from_user.id * 10 + int(id_message)
    cursor.execute('''DELETE FROM spreadsheet2 WHERE message_id = ?''', (message_id,))
    cursor.execute('''DELETE FROM spreadsheet1 WHERE message_id = ?''', (message_id,))
    sql_connection.commit()
    user_id = message.from_user.id
    message_id = cursor.execute('''SELECT message_id FROM spreadsheet1 WHERE user_id = ?''', (user_id,)).fetchall()
    quantity = cursor.execute('''SELECT COUNT(user_id) FROM spreadsheet1 WHERE user_id = ?''', (user_id,)).fetchone()
    mssg_id = []
    for i in list(message_id):
        mssg_id.append(i[0])
    for i in range(0,quantity[0]):
        mssg = message.from_user.id * 10 + i + 1
        cursor.execute('''UPDATE spreadsheet1 SET message_id = ? WHERE message_id = ?''', (mssg,mssg_id[i])).fetchone()
        cursor.execute('''UPDATE spreadsheet2 SET message_id = ? WHERE message_id = ?''', (mssg, mssg_id[i])).fetchone()
        sql_connection.commit()

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if(message.text == "/start"):
        bot.send_message(message.from_user.id,"Привет, " + message.from_user.first_name)
        bot.send_message(message.from_user.id,"Мои команды: \n/show - Повторить сообщения. \n/add - Добавить предыдущее сообщение. \n/delete Номер сообщения - удалить сообщение. \n/help")
    elif (message.text == "/help"):
        bot.send_message(message.from_user.id,"Мои команды: \n/show - Повторить сообщения \n/add - Добавить предыдущее сообщение. \n/delete Номер сообщения - удалить сообщение.")
    elif(message.text == "/show"):
        result = show_message(message)
        if not result:
            bot.send_message(message.from_user.id, "У тебя нет сообщений сохраненных")
        else:
            count = 1
            for i in list(result):
                mess = "Сообщение " + str(count) + " - " + str(i[0])
                bot.send_message(message.from_user.id,mess)
                count += 1
        print(type(result))
    elif (message.text == "/add"):
        add_msg(message)
    else:
        text = message.text.split()
        if(text[0] == "/delete"):
            delete_message(message, text[1])
        else:
            global record
            record = message.text
bot.polling(none_stop=True)