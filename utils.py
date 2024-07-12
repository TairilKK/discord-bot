import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

YT_LINK = ['https://www.youtube.com/watch?v=9woLRf94zCI',
           'https://www.youtube.com/watch?v=C21k7Id2_Wc']

load_dotenv()
TOKEN = os.getenv('TESTER_TOKEN')


def load_env_variables():
    """
    Loads environment varibles
    :return: Varibles from .env file
    """
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    number_of_words = os.getenv('NUMBER_OF_WORDS')
    return database_url, number_of_words


def db_open_connection(path):
    """
    Creates connection with database.
    :param path: Path to database.
    :return: database connection and dataabse cursor.
    """
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    return connection, cursor


def db_close_connection(connection):
    """
    Close the database connection.
    :param connection: Database connection.
    :return: Closed connection.
    """
    return connection.close()


def get_n_random_words(cursor, number_of_words):
    """
    Geting words from database.
    :param cursor: Database cursor.
    :param number_of_words: Number of random words.
    :return: Words tuple (word_id, word).
    """
    cursor.execute(f'SELECT WORD_ID, WORD '
                   f'FROM words '
                   f'WHERE USAGE = (SELECT MIN(USAGE) FROM words) '
                   f'ORDER BY RANDOM() '
                   f'LIMIT {number_of_words};')

    return cursor.fetchall()


def insert_words(cursor, words, table_name):
    """
    Inserts words to table.
    :param cursor: Database cursor.
    :param words: Words to insert.
    :param table_name: Table name.
    :return: Words tuple (word_id, word).
    """
    today = datetime.now()

    year = today.year
    month = today.month
    day = today.day

    query = f'INSERT INTO {table_name} (WORD_ID, DAY, MONTH, YEAR) VALUES (?, ?, ?, ?)'
    data_to_insert = [(word_id, day, month, year) for word_id, word in words]

    cursor.executemany(query, data_to_insert)
    cursor.connection.commit()

    return words


def daily_words(cursor, number_of_words):
    """
    Function get words and inserts to daily_word table.
    :param cursor: Database cursor.
    :param number_of_words: Number of random words.
    :return: Words tuple (word_id, word).
    """
    words = get_n_random_words(cursor, number_of_words)
    return insert_words(cursor, words, 'DAILY_WORDS')


def weekly_words(cursor, number_of_words):
    """
    Function get words and inserts to daily_word table.
    :param cursor: Database cursor.
    :param number_of_words: Number of random words.
    :return: Words tuple (word_id, word).
    """
    words = get_n_random_words(cursor, number_of_words)
    return insert_words(cursor, words, 'WEEKLY_WORDS')
