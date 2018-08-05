import requests
import itertools
import string

from multiprocessing import Pool
from sqlhelper import SQLUtils


# Define variables and connection to db
db_url = 'my_db.db'
db_table_name = 'helper'
sql = SQLUtils(db_url, db_table_name)

url = 'https://allo.ua/catalogsearch/ajax/suggest/{}'
question = "?q={}&currentTheme=main"
count_of_processing = 4


def generate_combinations(count=3):
    for number in range(1, count + 1):
        for combination in itertools.permutations(string.ascii_lowercase, number):
            yield ''.join(combination)


def get_helps(page_url, value):
    resp = requests.post(page_url.format(value))
    return resp.json()["query"]


def calculate_start_char(combinations, last_char=None):
    if last_char:
        while combinations.__next__() != last_char:
            pass


def make_all(chars):
    helps = get_helps(url, question.format(chars))
    sql.write(chars, ', '.join(helps))


def main():
    sql.create_table_if_not_exist()
    last_result = sql.get_last_processed_char()
    all_combinations = generate_combinations()
    calculate_start_char(all_combinations, last_result)

    with Pool(count_of_processing) as pool:
        pool.imap(make_all, all_combinations)
        pool.close()
        pool.join()


if __name__ == '__main__':
    main()
