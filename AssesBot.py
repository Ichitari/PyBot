import telebot
import sqlite3

connectionbase = sqlite3.connect('user.db') #Подключение к БД
bot = telebot.TeleBot('token')
cursor = connectionbase.cursor() #навигация по бд
name =''

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/Игра1', '/Игра2','/Игра3')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Да', 'Нет')

keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('Да', 'Нет')


keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard4.row("👍", "👎")

keyboard5 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard5.row('Да', 'Нет', 'зачем?')


@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, "Привет, меня зовут Игробот, а тебя?")
    bot.register_next_step_handler(message, get_name);

def get_name(message):  #
        global name;
        name = message.text;
        trop = "Приятно познакомиться," + name + ".Расскажи в какой из игры ты учавствовал"
        bot.send_message(message.from_user.id, trop, reply_markup=keyboard1)
        bot.register_next_step_handler(message, start_message1);

        global userId;
        userId = message.chat.id
        connectionbase = sqlite3.connect('/C:/sqlite/user.db')
        cursor = connectionbase.cursor()
        cursor.execute("INSERT INTO userj (userid, username) VALUES('" + str(message.chat.id) + "', '" + name + "')")
        connectionbase.commit()




@bot.message_handler(commands=['Игра1','Игра2','Игра3'])
def start_message1(message):
    play = message.text
    show = "Спасибо, что принял участие в игре" + play + "! Пожалуйста поделись своими впечатлениями"
    bot.send_message(message.chat.id, show)
    bot.register_next_step_handler(message, copy_txt);
    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()
    cursor.execute("UPDATE userj SET game = '" + str(message.text) + "' WHERE username = '" + name + "'")
    connectionbase.commit()


def copy_txt(message):
    global otzv;
    otzv = "/" +message.text;
    print(otzv)
    bot.send_message(message.chat.id, "Благодарю за отзыв. Хочешь немного интерактива?",reply_markup=keyboard2)
    bot.register_next_step_handler(message, interactiv_flow);
    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()
    cursor.execute("UPDATE userj SET opinion = '" + str(message.text) + "' WHERE username = '" + name + "'")
    connectionbase.commit()

def interactiv_flow(message):

    if message.text == "да":
        bot.send_message(message.from_user.id, "Я уверен, ты знаешь что такое лайки и не раз их ставил. Я спрошу у тебя о некоторых вещах связанных с мероприятием, а ты просто ставь like или dislike. Готов?",reply_markup=keyboard3);

        bot.register_next_step_handler(message, choise_1);
    elif message.text == "Да":
            bot.send_message(message.from_user.id, "Я уверен, ты знаешь что такое лайки и не раз их ставил. Я спрошу у тебя о некоторых вещах связанных с мероприятием, а ты просто ставь like или dislike. Готов?",reply_markup=keyboard3);
            bot.register_next_step_handler(message, choise_1);

    else:
        bot.send_message(message.from_user.id, 'Твой чат - твои правила. Если вдруг передумаешь просто напиши start и мы попробуем сначала.');

def choise_1(message):

    bot.send_message(message.chat.id, "Вводная лекция была достаточно понятна?",reply_markup=keyboard4)
    bot.register_next_step_handler(message, choise_2);
def choise_2(message):
    bot.send_message(message.chat.id, "Оцени атмосферу в целом", reply_markup=keyboard4)
    bot.register_next_step_handler(message, choise_3);

    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()


    if message.text == '👍':

     cursor.execute("UPDATE userj SET lection = 'Хорошо' WHERE username = '" + name + "'")
     connectionbase.commit();

    if message.text == '👎':

     cursor.execute("UPDATE userj SET lection = 'Плохо' WHERE username = '" + name + "'")
     connectionbase.commit();


def choise_3(message):
    bot.send_message(message.chat.id, "Волвлеченность в игровой процесс", reply_markup=keyboard4)
    bot.register_next_step_handler(message, choise_4);

    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()

    if message.text == '👍':
        cursor.execute("UPDATE userj SET atmosphere = 'Хорошо' WHERE username = '" + name + "'")
        connectionbase.commit();

    if message.text == '👎':
        cursor.execute("UPDATE userj SET atmosphere = 'Плохо' WHERE username = '" + name + "'")
        connectionbase.commit();


def choise_4(message):
    bot.send_message(message.chat.id, "Как тебе работа тех. поддержки?", reply_markup=keyboard4)
    bot.register_next_step_handler(message, number_phone);

    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()

    if message.text == '👍':
        cursor.execute("UPDATE userj SET linegame = 'Хорошо' WHERE username = '" + name + "'")
        connectionbase.commit();

    if message.text == '👎':
        cursor.execute("UPDATE userj SET linegame = 'Плохо' WHERE username = '" + name + "'")
        connectionbase.commit();


def number_phone(message):
    bot.send_message(message.chat.id, "Интересная наверно была игра) Обменяемся номерами?", reply_markup=keyboard5)
    bot.register_next_step_handler(message, number_phone2);

    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()

    if message.text == '👍':
        cursor.execute("UPDATE userj SET support = 'Хорошо' WHERE username = '" + name + "'")
        connectionbase.commit();

    if message.text == '👎':
        cursor.execute("UPDATE userj SET support = 'Плохо' WHERE username = '" + name + "'")
        connectionbase.commit();

def number_phone2(message):
 if message.text == "Да":
     bot.send_message(message.chat.id, "Классно, вот мой:+7929*******. жду твой ")
     bot.register_next_step_handler(message, number_phone3);


 elif message.text == "Нет":
     bot.send_message(message.chat.id, "Настаиваеть не буду) Спасибо за общение.")
     #Выходим из цикла
 elif message.text == "зачем?":
     bot.send_message(message.chat.id, "Возможно именно твой отзыв поможет нам делать игру более приятной. В этом случае, номер просто необходим для обратной связи. Обменяемся номерами?", reply_markup=keyboard3)
     bot.register_next_step_handler(message, number_phone0);

def number_phone3(message):
    bot.send_message(message.chat.id, "Сохранил номер) До связи")
    connectionbase = sqlite3.connect('/C:/sqlite/user.db')
    cursor = connectionbase.cursor()
    cursor.execute("UPDATE userj SET phone = '" + str(message.text) + "' WHERE username = '" + name + "'")

    # cursor.execute("UPDATE userq WHERE userid =('" + str(message.chat.id) + "') VALUES ('" + str(message.text) + "')")
    connectionbase.commit()
    #выход из цикла
def number_phone0(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, "Классно, вот мой:+7929*******. жду твой ")
        bot.register_next_step_handler(message, number_phone3);
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Настаивать не буду) Спасибо за общение.")
0bot.polling(none_stop=True)

