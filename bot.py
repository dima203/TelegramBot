# ---------------------------------------------------------------------------------------------------------------------
#                   Bot by dima203
#               @TestMyNewTelegramBot
# ---------------------------------------------------------------------------------------------------------------------
from config import BOT
from handlers import *


def main():
    try:
        BOT.polling()
    except Exception as e:
        print(e)
    finally:
        print(1)
        config.DATABASE.safe_changes()


if __name__ == '__main__':
    main()
