import pandas as pd
from img_dwl import get_link, save_image
import sqlite3

mydb = sqlite3.connect('anime.db')
mycursor = mydb.cursor()


def create_base(mycursor):
    sql = 'CREATE DATABASE IF NOT EXISTS anime '
    mycursor.execute(sql)
# (user_id INT AUTO_INCREMENT PRIMARY KEY, user_winner_list VARCHAR(250))


def create_table(mycursor):
    sql = 'CREATE TABLE IF NOT EXISTS animemash(anime_id INT PRIMARY KEY, anime_name VARCHAR(250), anime_rate float, anime_image VARCHAR(250))'
    mycursor.execute(sql)
    mydb.commit()
    sql = 'CREATE TABLE IF NOT EXISTS anime_users (user_id_anime INT PRIMARY KEY, user_winner_list VARCHAR)'
    mycursor.execute(sql)
    mydb.commit()


def get_anime_info():
    print("Запущен процесс чтения csv")
    anime_df = pd.read_csv("anime/anime.csv")
    anime_df["Аниме"].dropna(inplace=True)
    anime = anime_df["Аниме"].to_list()
    for index, item in enumerate(anime):
        anime[index] = (index+1, item, '500', get_link(item))
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
    sql = """INSERT INTO animemash (anime_id,anime_name, anime_rate, anime_image) VALUES (?, ?, ?, ?)"""
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
    create_table(mycursor)
    anime = get_anime_info()
    fill_base_anime(anime, mycursor, mydb)
    print_base(mycursor)


if __name__ == '__main__':
    main()
