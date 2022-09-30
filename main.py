import sqlite3
import telebot

date = 0
day = 0
mas = []
bot = telebot.TeleBot('');
time = 0
cost = 0
del_flag = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "/reg чтобы ввести значение\n")
        bot.send_message(message.from_user.id, "/del чтобы удалить значение\n")
        bot.send_message(message.from_user.id, "/fix чтобы исправить значение, которые вы ввели\n")
        bot.send_message(message.from_user.id, "/printall чтобы посмотреть доходы за месяц\n")
        bot.send_message(message.from_user.id, "/printsum чтобы вывести сумму за месяц\n")
    elif message.text == "/reg":
        global del_flag
        del_flag = 0
        bot.send_message(message.from_user.id, "Введите число")
        bot.register_next_step_handler(message, get_date)
    elif message.text == "/del":
        del_flag = 1
        bot.send_message(message.from_user.id, "Введите число")
        bot.register_next_step_handler(message, get_date)
    elif message.text == "/fix":
        del_flag = 2
        bot.send_message(message.from_user.id, "Введите число")
        bot.register_next_step_handler(message, get_date)
    elif message.text == "/printsum":
        print_sum(message)
    elif message.text == "/printall":
        print_all(message)
    else:
        bot.send_message(message.from_user.id, "Введите /help чтобы получить помощь")


def get_date(message):
    global date
    date = message.text
    if ((int(date) >= 1) and (int(date) <= 31)):
        bot.send_message(message.from_user.id, "Введи номер дня(одно число от 1 до 7)")
        print(date)
        bot.register_next_step_handler(message, get_day)
    else:
        bot.send_message(message.from_user.id, "Вы ввели число неправильно, пожалуйста введите число еще раз")
        bot.register_next_step_handler(message, get_date)


def get_day(message):
    global day
    day = message.text
    if ((int(date) >= 1) and (int(date) <= 7)):
        #print()
        bot.send_message(message.from_user.id, "Какое время(в формате hh:mm)?")
        bot.register_next_step_handler(message, get_time)
    else:
        bot.send_message(message.from_user.id,
                         "Вы ввели день неправильно, пожалуйста введите день(одно число от 1 до 7) еще раз")
        bot.register_next_step_handler(message, get_date)


def get_time(message):
    global time;
    time = message.text;
    flag = 0
    if (len(time) != 5):
        flag = 1
    else:
        for i in range(0, 5, 1):
            if ((i == 2) and ((time[i] != ':'))):
                flag = 1
            elif ((i != 2) and ((time[i] < '0') or (time[i] > '9'))):
                flag = 1
    if flag == 0:
        bot.send_message(message.from_user.id, "Сколько заработаешь?")
        bot.register_next_step_handler(message, get_cost)
    else:
        bot.send_message(message.from_user.id,
                         "Вы ввели время неправильно, пожалуйста введите время(в формате hh:mm) еще раз")
        bot.register_next_step_handler(message, get_time)


def get_cost(message):
    global del_flag
    global cost
    cost = message.text
    if int(cost) >= 0:
        if (del_flag == 1):
            del_data(message)
        elif (del_flag == 2):
            fix_data(message)
        else:
            mas.append([date, day, time, cost])
            bot.send_message(message.from_user.id, "Записалось")
            bot.send_message(message.from_user.id, "Введите /help чтобы получить помощь")
    else:
        bot.send_message(message.from_user.id,
                         "Вы ввели прибыль неправильно, пожалуйста введите прибыль(целое число) еще раз")
        bot.register_next_step_handler(message, get_cost)


def print_sum(message):
    global cost
    cost = int(0)
    for i in range(0, len(mas), 1):
        cost += int(mas[i][3])
    res = "За месяц вы заработали "
    res += str(cost)
    bot.send_message(message.from_user.id, res)
    bot.send_message(message.from_user.id, "Введите /help чтобы получить помощь")


def from_num_to_day(num):
    global day;
    day = num;
    day = int(day)
    # print("we here and day =", day)
    if day == 1:
        return "Понедельник"
    elif day == 2:
        return "Вторник";
    elif day == 3:
        return "Среда";
    elif day == 4:
        return "Четверг";
    elif day == 5:
        return "Пятница";
    elif day == 6:
        return "Суббота";
    elif day == 7:
        return "Воскресенье"


def print_all(message):
    res = ""
    for i in range(0, len(mas), 1):
        res += mas[i][0]
        res += ' '
        res += from_num_to_day(mas[i][1])
        res += ' '
        res += mas[i][2]
        res += ' '
        res += mas[i][3]
        res += '\n'
    bot.send_message(message.from_user.id, res)


def del_data(message):
    flag = 0
    #print(date, day, time, cost)
    for i in range(0, len(mas), 1):
        if ((mas[i][0] == date) and (mas[i][1] == day) and (mas[i][2] == time) and (mas[i][3] == cost)):
            mas.remove([date, day, time, cost])
            bot.send_message(message.from_user.id, "Нашел и удалил")
            flag = 1
    if flag == 0:
        bot.send_message(message.from_user.id, "Не нашел")
    bot.send_message(message.from_user.id, "Введите /help чтобы получить помощь")


def fix_data(message):
    flag = 0
    global del_flag
    for i in range(0, len(mas), 1):
        if ((mas[i][0] == date) and (mas[i][1] == day) and (mas[i][2] == time) and (mas[i][3] == cost)):
            mas.remove([date, day, time, cost])
            bot.send_message(message.from_user.id, "Нашел, введите правильные данные после следующего сообщения")
            del_flag = 0
            bot.send_message(message.from_user.id, "Введите число")
            bot.register_next_step_handler(message, get_date)
            flag = 1
    if flag == 0:
        bot.send_message(message.from_user.id, "Не нашел")
        bot.send_message(message.from_user.id, "Введите /help чтобы получить помощь")


bot.polling(none_stop=True, interval=0)
