import string
import random


def garbage():
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=20))
    return str(res)
