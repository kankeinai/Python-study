import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check api")
    return res


def get_num_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1pass = (hashlib.sha1(password.encode('utf-8')).hexdigest()).upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5_char)
    return get_num_leaks(response, tail)


def main(argvs):
    for password in argvs:
        count = pwned_api_check(password)
        if count:
            print(
                f"Password: {password} was leaked {count} times\nPress F to pay respect and change it")
        else:
            print(f"Password: {password} was not found")
    return 'done'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
