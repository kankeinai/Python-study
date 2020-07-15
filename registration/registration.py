import re
import os
import email_sender
import random_code
import password as checker

base = {}
pattern_email = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pattern_password = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d_\-]{6,20}$")
try:
    with open("registration.txt", 'r+') as reg:
        if(os.stat("registration.txt").st_size):
            for lines in reg:
                base[lines.split(" ")[0]] = lines.split(" ")[1]
except FileNotFoundError:
    file = open("registration.txt", 'w').close()
while True:
    print("WELCOME to Registartion")
    while True:
        mail = input("Please enter your mail in the right format: ")
        if re.search(pattern_email, mail):
            if mail not in base:
                while True:
                    code = random_code.garbage()
                    email_sender.confirm(mail, code)
                    answer = input(
                        "The code was sent to your mail to confirm it, paste it here: ")
                    if answer == code:
                        while True:
                            password = input("Enter password: ")
                            if re.search(pattern_password, password):
                                count = checker.pwned_api_check(password)
                                if count:
                                    print(
                                        f"This password was hacked {count} times. Choose a different one")
                                else:
                                    print("Your password is good")
                                    base[mail] = password
                                    with open("registration.txt", 'a+') as reg:
                                        reg.writelines(f"{mail} {password} \n")
                                    print("You have succefully registered")
                                    break
                            else:
                                print("Password is in the wrong format")
                        break
                    else:
                        print("Wrong code. The email was not confirmed.")
                        break
            else:
                tries = 5
                print("The entered email is already registered. \nYou can login instead")
                while 1:
                    if tries > 0:
                        password = input("Enter password: ")
                        if base[mail] == password:
                            print("You have succesefully logined")
                            tries = 5
                            break
                        else:
                            tries -= 1
                            print(
                                f"Wrong password. You still have {tries}", end=' ')
                            if tries == 1:
                                print("try")
                            else:
                                print("tries")
                    else:
                        respond = input(
                            "Would u like to restore your password? 1 for yes: ")
                        if respond == '1':
                            code = random_code.garbage()
                            email_sender.restore(mail, code)
                            answer = input("Please paste code here: ")
                            if answer == code:
                                print(
                                    f"\nYour login data\nmail: {mail}\npassword: {base[mail]}")
                                break
                        print("The access is prohibited")
                        break
            break
        else:
            print("The mail is not in the right format")
    respond = input("Would u like to register one more account. 0 to exit: ")
    if respond == '0':
        break
print("Bye.")
