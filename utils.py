import os
import random
import sqlite3

from datetime import datetime
from dotenv import load_dotenv
from typing import List, Tuple


def load_env_variables() -> Tuple[str, int, str, str]:
  """
  Loads environment varibles

  :return: Varibles from .env file
  """
  load_dotenv()
  database_url = os.getenv('DATABASE_URL')
  number_of_words = os.getenv('NUMBER_OF_WORDS')
  TOKEN = os.getenv('TESTER_TOKEN')
  SONGS_DB_URL = os.getenv('SONGS_DB_URL')

  return database_url, number_of_words, TOKEN, SONGS_DB_URL


def db_open_connection(path: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
  """
  Creates connection with database.

  :param path: Path to database.
  :return: database connection and dataabse cursor.
  """
  connection = sqlite3.connect(path)
  cursor = connection.cursor()
  return connection, cursor


def db_close_connection(connection: sqlite3.Connection) -> sqlite3.Connection:
  """
  Close the database connection.

  :param connection: Database connection.
  :return: Closed connection.
  """
  return connection.close()


def get_n_random_words(cursor: sqlite3.Cursor, number_of_words: int) -> List[Tuple[int, str]]:
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


def insert_words(cursor: sqlite3.Cursor, words: List[Tuple[int, str]], table_name: str):
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


def daily_words(cursor: sqlite3.Cursor, number_of_words: int):
  """
  Function get words and inserts to daily_word table.

  :param cursor: Database cursor.
  :param number_of_words: Number of random words.
  :return: Words tuple (word_id, word).
  """
  words = get_n_random_words(cursor, number_of_words)
  return insert_words(cursor, words, 'DAILY_WORDS')


def weekly_words(cursor: sqlite3.Cursor, number_of_words: int):
  """
  Function get words and inserts to daily_word table.

  :param cursor: Database cursor.
  :param number_of_words: Number of random words.
  :return: Words tuple (word_id, word).
  """
  words = get_n_random_words(cursor, number_of_words)
  return insert_words(cursor, words, 'WEEKLY_WORDS')


def get_random_song_from_directory(directory: str) -> str:
    """Pobiera losową ścieżkę do pliku mp3 z podanego katalogu."""
    files = [f for f in os.listdir(directory) if f.endswith('.mp3')]
    if not files:
        raise FileNotFoundError("No mp3 files found in the directory.")
    return os.path.join(directory, random.choice(files))
