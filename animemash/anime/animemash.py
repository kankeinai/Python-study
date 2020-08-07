from math import pow
from random import randint
import mysql.connector

# db anime, table animemash
# anime_id, anime_name, anime_rate(default=500), anime_image
# Получаем названия Аниме из .csv, ссылки на картинки с помощью get_link()
# Первое - предыдущий победитель, второе - рандом


def gener_anime(size, anime_list, winner_list):
    print(anime_list)
    anime_one = anime_list[randint(0, size-1)]
    anime_two = anime_list[randint(0, size-1)]
    while True:
        if (anime_one == anime_two) or ():
            anime_two = anime_list[randint(0, size-1)]
        else:
            break
    return anime_one, anime_two

# Выбираем лучшее аниме


def choose_best_anime(anime_one, anime_two, mycursor):
    sql = '''SELECT * FROM animemash WHERE anime_id =%s'''
    mycursor.execute(sql, (anime_one,))
    result_1 = mycursor.fetchall()
    sql = '''SELECT * FROM animemash WHERE anime_id =%s'''
    mycursor.execute(sql, (anime_two,))
    result_2 = mycursor.fetchall()
    return result_1, result_2


def get_Expectation(rate_1, rate_2):
    calc = float(
        1.0 / (1.0 + pow(10, ((float(rate_2) - float(rate_1)) / 400))))
    print(calc)
    return calc


def modifyRating(rating, expected, actual, kfactor):
    calc = (float(rating) + kfactor * (float(actual) - float(expected)))
    print(calc)
    return calc

# Считаем новый рейтинг


def get_new_rates(winner, result_1, result_2, result_1_rate, result_2_rate):
    exp_A = get_Expectation(result_1_rate, result_2_rate)
    exp_B = get_Expectation(result_2_rate, result_1_rate)
    if winner == result_1:
        new_rate_A = modifyRating(result_1_rate, exp_A, 1, 30)
        new_rate_B = modifyRating(result_2_rate, exp_B, -1, 30)
    else:
        new_rate_B = modifyRating(result_2_rate, exp_B, 1, 30)
        new_rate_A = modifyRating(result_1_rate, exp_A, -1, 30)
    return new_rate_A, new_rate_B

# Обновляем данные бд


def update_rates(new_rate_A, anime_one, new_rate_B, anime_two, mycursor, mydb):
    sql = "UPDATE animemash SET anime_rate=%s WHERE anime_id=%s"
    mycursor.execute(sql, (new_rate_A, anime_one))
    sql = "UPDATE animemash SET anime_rate=%s WHERE anime_id=%s"
    mycursor.execute(sql, (new_rate_B, anime_two))
    mydb.commit()
# Выводим топ-10


def show_rates(mycursor):
    sql = '''SELECT * FROM animemash ORDER BY anime_rate DESC LIMIT 10'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    index = 1
    rating = ''
    for x in myresult:
        rating += (f"{index}. {x[1]}\n")
        index += 1
    return rating
# Обнуляем всем рейтинг


def random_phrase(user_name):
    phrases = [", интересный выбор. ", ", наверно стоит посмотреть. ", f"? {user_name}, расскажи потом о чем оно, интересно. ", ", неожиданно. ", f"? {user_name}, ты немного предсказуем. ", "? Так и знала и как я не догадалась... ",
               "? Я выбрал бы тоже самое. ", f"? А я вижу в {user_name} задатки отаку.\n", f"? {user_name}, отличный выбор! ", ", *туц*  ", f"? {user_name}, отвечаешь как профессиональный анимешник. ", "? Тоже его люблю. ", "? Не останавливайся, ещё есть что выбрать. "]
    return phrases[randint(0, 12)]
