import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mikael-love",
    database="anime"
)
mycursor = mydb.cursor()


def create_base(mycursor):
    try:
        sql = 'CREATE DATABASE anime'
        mycursor.execute(sql)
    except:
        print("База данных существует")
# (user_id INT AUTO_INCREMENT PRIMARY KEY, user_winner_list VARCHAR(250))


def create_table(mycursor):
    sql = 'CREATE TABLE anime_users(user_id_anime INT, user_winner_list VARCHAR(250))'
    mycursor.execute(sql)
    mydb.commit()


def get_anime_info():
    print("Запущен процесс чтения csv")
    anime_df = pd.read_csv("anime/anime.csv")
    anime_df["Аниме"].dropna(inplace=True)
    anime = anime_df["Аниме"].to_list()
    for index, item in enumerate(anime):
        anime[index] = (item, '500', get_link(item))
    return anime


def delete_all_rows(mycursor, mydb):
    print("Запущен процесс очищения базы данных")
    sql = 'DELETE FROM animemash'
    mycursor.execute(sql)
    sql = ' ALTER TABLE animemash AUTO_INCREMENT=0'
    mycursor.execute(sql)
    mydb.commit()


def fill_base_anime(anime, mycursor, mydb):
    print("Запущен процесс заполнения базы данных")
    sql = """INSERT INTO animemash (anime_name, anime_rate, anime_image) VALUES (%s, %s, %s)"""
    mycursor.executemany(sql, anime)
    mydb.commit()


def refresh(mycursor, mydb):
    sql = "UPDATE animemash SET anime_rate='500'"
    mycursor.execute(sql)
    mydb.commit()


def print_base(mycursor):
    print("Table anime:")
    sql = '''SELECT * FROM animemash ORDER BY anime_rate DESC'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(f"{x[0]}. {x[1]} - {x[2]}, url:{x[3]}")


def main():
    sql = "drop table anime_users"
    mycursor.execute(sql)
    mydb.commit()
    create_table(mycursor)


if __name__ == '__main__':
    main()
