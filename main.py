import os
from utils import *


def main():
    database_url, number_of_words = load_env_variables()
    conn, c = db_open_connection(database_url)

    words = daily_words(c, 4)

    db_close_connection(conn)


if __name__ == '__main__':
    main()
