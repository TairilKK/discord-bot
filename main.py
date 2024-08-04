from bot import setup
from utils import *


def main():
  database_url, number_of_words, TOKEN, SONGS_DB_URL = load_env_variables()
  bot, t = setup(TOKEN, SONGS_DB_URL)


if __name__ == '__main__':
  main()
