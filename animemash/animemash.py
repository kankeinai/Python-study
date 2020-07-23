from math import pow
import mysql.connector
from random import randint
from img_dwl import save_image, get_link
from admin_anime import get_anime_info, delete_all_rows, fill_base_anime, refresh, print_base


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mikael-love",
    database="anime"
)
mycursor = mydb.cursor()

# db anime, table animemash
# anime_id, anime_name, anime_rate(default=500), anime_image

# Получаем названия Аниме из .csv, ссылки на картинки с помощью get_link()

# Первое - предыдущий победитель, второе - рандом


def generate_anime(winner, rows):
    anime_one = winner
    anime_two = randint(1, rows)
    while True:
        if anime_one == anime_two:
            anime_two = randint(1, rows)
        else:
            break
    return anime_one, anime_two

# Выбираем лучшее аниме


def choose_best_anime(anime_one, anime_two):
    sql = '''SELECT * FROM animemash WHERE anime_id =%s'''
    mycursor.execute(sql, (anime_one,))
    result_1 = mycursor.fetchall()
    sql = '''SELECT * FROM animemash WHERE anime_id =%s'''
    mycursor.execute(sql, (anime_two,))
    result_2 = mycursor.fetchall()
    anime_image_one = save_image(result_1[0][1], result_1[0][3])
    anime_image_two = save_image(result_2[0][1], result_2[0][3])
    anime_image_one.show()
    anime_image_two.show()
    response = input(
        f"Which anime is better:\n1. {result_1[0][1]}\n2. {result_2[0][1]}\nОтвет: ")
    # вызываем функцию save_image() если картинки нет в папке, она скачает
    # как-нибудь эти картинки открываем
    anime_image_one.close()
    anime_image_two.close()
    return result_1, result_2, response


def get_Expectation(rate_1, rate_2):
    calc = (1.0 / (1.0 + pow(10, ((rate_2 - rate_1) / 400))))
    return calc


def modifyRating(rating, expected, actual, kfactor):
    calc = (rating + kfactor * (actual - expected))
    return calc

# Считаем новый рейтинг


def get_new_rates(response, result_1, result_2, anime_one, anime_two):
    exp_A = get_Expectation(result_1[0][2], result_2[0][2])
    exp_B = get_Expectation(result_2[0][2], result_1[0][2])
    if response == '1':
        new_rate_A = modifyRating(result_1[0][2], exp_A, 1, 5)
        new_rate_B = modifyRating(result_2[0][2], exp_B, 0, 5)
        winner = anime_one
    else:
        new_rate_B = modifyRating(result_2[0][2], exp_B, 1, 5)
        new_rate_A = modifyRating(result_1[0][2], exp_A, 0, 5)
        winner = anime_two
    return new_rate_A, new_rate_B, winner

# Обновляем данные бд


def update_rates(new_rate_A, anime_one, new_rate_B, anime_two):
    sql = "UPDATE animemash SET anime_rate=%s WHERE anime_id=%s"
    mycursor.execute(sql, (new_rate_A, anime_one))
    sql = "UPDATE animemash SET anime_rate=%s WHERE anime_id=%s"
    mycursor.execute(sql, (new_rate_B, anime_two))
    mydb.commit()
# Выводим топ-10


def show_rates():
    sql = '''SELECT * FROM animemash ORDER BY anime_rate DESC LIMIT 10'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    index = 1
    for x in myresult:
        print(f"{index}. {x[1]}")
        index += 1

# Обнуляем всем рейтинг


def main():
    print_base(mycursor)
    mycursor.execute("SELECT COUNT(*) FROM animemash")
    myresult = mycursor.fetchall()
    rows = myresult[0][0]
    mycursor.execute("SELECT anime_id FROM animemash LIMIT 1")
    myresult = mycursor.fetchall()
    winner = myresult[0][0]
    while True:
        # generate 2 anime
        anime_one, anime_two = generate_anime(winner, rows)
        # save user's choice
        result_1, result_2, response = choose_best_anime(anime_one, anime_two)
        # generate new rates
        new_rate_A, new_rate_B, winner = get_new_rates(
            response, result_1, result_2, anime_one, anime_two)
        # save them to the database
        update_rates(new_rate_A, anime_one, new_rate_B, anime_two)
        # Функция показать топ
        response = input("Генерировать аниме? 1. да\n")
        if response != '1':
            break
    show_rates()


if __name__ == '__main__':
    main()
