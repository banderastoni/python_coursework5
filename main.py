import os

import colorama

from utils.utils import *
from config import config

companies = {
    2324020: "Точка",
    3776: "МТС",
    9819865: "Сбербанк СБМ",
    15478: "VK",
    8178: "TeleForm",
    8620: "RAMBLER&CO",
    4920624: "SelfSec",
    80660: "Boxberry",
    1455: "HH",
    864086: "getmatch",
}
DB_NAME = 'vacancies'
params = config()
script_file = os.path.join('scripts', 'queries.sql')

if __name__ == '__main__':
    list_ = get_vacancies(companies)
    create_db(DB_NAME, params)
    print(colorama.Fore.GREEN + 'База данных создана...' + colorama.Fore.RESET)
    params.update({'dbname': DB_NAME})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_tables(cur, script_file)
                print(colorama.Fore.GREEN + f"Таблицы в БД {DB_NAME} успешно созданы..." + colorama.Fore.RESET)

                fill_table_companies(cur, companies)
                print(colorama.Fore.GREEN + "Таблица companies заполнена..." + colorama.Fore.RESET)

                fill_table_vacancies(cur, list_)
                print(colorama.Fore.GREEN + "Таблица vacancies заполнена..." + colorama.Fore.RESET)

                add_foreign_key(cur)
                print(colorama.Fore.GREEN + "Связывание таблиц успешно..." + colorama.Fore.RESET)

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    user_interaction(params)
