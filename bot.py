# ---------------------------------------------------------------------------------------------------------------------
#                   Bot by dima203
#               @TestMyNewTelegramBot
# ---------------------------------------------------------------------------------------------------------------------
from handlers import *
from timer import RepeatedTimer


def heal():
    for i in DATABASE.players:
        if not DATABASE.players[i].is_death:
            DATABASE.players[i].heal()


# Основной цикл
def main():
    try:
        timer = RepeatedTimer(1, heal)
        timer.start()

        # Запуск цикла
        BOT.polling()
    except Exception as e:
        # Вызов ошибки при наличии
        raise e
    finally:
        timer.stop()

        # При завершении сохранить БД
        DATABASE.safe_changes()


if __name__ == '__main__':
    main()
