import pandas
import mysql.connector


def create_base(mycursor):
    try:
        sql = 'CREATE DATABASE anime'
        mycursor.execute(sql)
    except:
        print("База данных существует")


def create_table(mycursor):
    try:
        sql = 'CREATE TABLE animemash (anime_id INT AUTO_INCREMENT PRIMARY KEY , anime_name VARCHAR(250), anime_rate INT, anime_image VARCHAR(250)) '
        mycursor.execute(sql)
    except:
        print("Таблица существует")


def get_anime_info():
    print("Запущен процесс чтения csv")
    anime_df = pd.read_csv("anime.csv")
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
    sql = '''SELECT * FROM animemash'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(f"{x[0]}. {x[1]} - {x[2]}, url:{x[3]}")
