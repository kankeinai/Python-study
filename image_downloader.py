import requests
import sys
import pprint
import os
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter
import zipfile

url = 'https://my.nu.edu.kz/.PhoneBookPortlet/UsernameServlet?type=getphoto&uid='


def parser(document):
    with open(document, 'rb') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        links = soup.select('.rowClass.onetee')
        images_list = []
        for idx, items in enumerate(links):
            link = links[idx].get('uid', None)
            names = links[idx].select('a')
            name = names[0].getText().split('/')[0]
            email = name.split(" ")[0]+"."+name.split(" ")[1]+"@nu.edu.kz"
            images_list.append({'id': link, 'name': names[0].getText().split(
                '/')[0], 'link': url+link, 'email': email.lower()})
        return images_list


def get_file(url):
    r = requests.get(url, stream=True)
    return r


def save_image(name, file_object):
    with open(name, 'bw') as file:
        for chunk in file_object.iter_content(8192):
            file.write(chunk)


def parse_images_school(new_folder, students_list):
    response = input(
        f"Вы точно хотите выгрузить фото школы {new_folder.split('/')[-1].upper()}? (1. да): ")
    if response == '1':
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)
        response = input("Сортировать по годам? (1. да): ")
        for item in students_list:
            if response == '1':
                my_folder = new_folder+"/"+item['id'][:4]
                if not os.path.exists(my_folder):
                    os.mkdir(my_folder)
            else:
                my_folder = new_folder
            save_image(my_folder + "/" +
                       item['id'] + '.jpg', get_file(item['link']))
    response = input("Архивировать все фото? (1. да): ")
    if response == '1':
        archiev(new_folder, new_folder.split("/")[-1])


def archiev(folder, name):
    zip_file = zipfile.ZipFile(folder + '/' + name + '.zip', 'w')
    for folder, subfolders, files in os.walk(folder + '/'):
        for file in files:
            if file.endswith('.jpg'):
                zip_file.write(os.path.join(folder, file), os.path.relpath(
                    os.path.join(folder, file), folder + '/'), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()


def main():
    schools = ['cps', 'seds', 'ssh', 'smg']
    if not os.path.exists("images"):
        os.mkdir("images")
    print("Добро пожаловать в базу студентов NU")
    print("Выберите действие:")
    response = input(
        '1. Выгрузить фото со всех школ\n2. Выгрузить фото одной из школ\n3. Выгрузить фото определенного студента\n4. Получить информацию о всех студентах\n')
    if response == '1':
        students_list = []
        for item in schools:
            new_folder = "images/" + item
            students_list.append(
                {'school': item, 'students': parser("schools/" + item + ".html")})
            parse_images_school(new_folder, students_list)
            pprint(f"{item.upper()} готова")

    if response == '4':
        students_list = []
        for item in schools:
            new_folder = "images/" + item
            students_list.append(
                {'school': item, 'students': parser("schools/" + item + ".html")})
        print(students_list)

    if response == '2' or response == '3':
        while True:
            school = input("Введите школу: CPS, SEDS, SSH или SMG\n").lower()
            if school not in schools:
                print("Школа не найдена")
            else:
                break

    if response == '2':
        new_folder = "images/"+school
        students_list = parser("schools/" + school + ".html")
        parse_images_school(new_folder, students_list)

    if response == '3':
        student = input("Введите имя или student id: ")
        students_list = parser("schools/" + school + ".html")
        check = True
        for item in students_list:
            if student == item['name'] or student == item['id']:
                save_image(item['id'] + '.jpg', get_file(item['link']))
                Image.open(item['id'] + '.jpg').show()
                check = False
                return
        if check:
            print("Студент не найден")


if __name__ == '__main__':
    main()
