from translate import Translator


print("Welcome to offline translator!")
while True:
    print("Before choosing the language, make sure that you have found the right lang code (see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)")
    lang = input("\nInput lang code: ")
    translation = Translator(to_lang=lang)
    respond = input(
        "Please choose a working mode:\n1. From a keyboard\n2. From a text file\nOther to exit\n")
    if respond == '1':
        text = input("Please insert your text there:\n")
        print("\nTranslation:")
        print(translation.translate(text))
    elif respond == '2':
        while True:
            file_name = input("Please write the name of your file: ")
            try:
                with open(file_name) as input_file:
                    with open('output.txt', 'w') as output_file:
                        print("The file output.txt is created\n")
                        for line in input_file:
                            trans_line = translation.translate(line)
                            output_file.writelines(trans_line)
                            print(trans_line)
                        break
            except FileNotFoundError:
                print(
                    "File is not found, consider ckecking the rightness of spelling the name of your file")
    else:
        break
    ans = input(
        "\nThe translation is over. Would u like to continue? Write 0 for exit: ")
    if ans == '0':
        break
print("Bye.")
