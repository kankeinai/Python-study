import re
base = {}
pattern_email = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pattern_password = re.compile(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_\-])[A-Za-z\d_\-]{6,20}$")
while 1:
    print("WELCOME to Registartion")
    mail = input("Please enter your mail in the right format: ")
    if re.search(pattern_email, mail):
        if mail not in base:
            while 1:
                password = input("Enter password: ")
                if re.search(pattern_password, password):
                    base[mail] = password
                    print("You have succefully registered")
                    break
                else:
                    print("Password is in the wrong format")
        else:
            tries = 5
            print("The entered email is already registered. \nYou can login instead")
            while 1:
                if tries != 0:
                    password = input("Enter password: ")
                    if base[mail] == password:
                        print("You have succesefully logined")
                        tries = 5
                    else:
                        tries -= 1
                        if tries == 1:
                            print(
                                "Wrong password. You still have {} try".format(tries))
                        else:
                            print(
                                "Wrong password. You still have {} tries".format(tries))
                else:
                    print("The access is prohibited")
                    break
    respond = input("Would u like to register one more account. 0 to exit: ")
    if respond == '0':
        break
print("Bye.")
