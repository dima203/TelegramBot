# ---------------------------------------------------------------------------------------------------------------------
#                   Bot by dima203
#               @TestMyNewTelegramBot
# ---------------------------------------------------------------------------------------------------------------------
from handlers import *
from timer import RepeatedTimer


# Функция лечения игроков
def heal():
    for i in DATABASE.players:
        if not DATABASE.players[i].is_death:
            DATABASE.players[i].heal()


# Основной цикл
def main():

    # Проверка наличия изменений в классе игрока
    local_player = Player()
    for i in DATABASE.players:
        for attr in dir(local_player):
            if hasattr(DATABASE.players[i], attr):
                DATABASE.players[i].attr = eval(f'local_player.{attr}')
    del local_player

    # Создание таймера для лечения игроков
    timer = RepeatedTimer(1, heal)
    try:
        # Старт таймера для лечения игроков
        timer.start()
        # Запуск цикла
        BOT.polling()

    except Exception as e:
        # Вызов ошибки при наличии
        raise e

    finally:
        # Остановка таймера для лечения игроков
        timer.stop()

        # При завершении сохранить БД
        DATABASE.safe_changes()


if __name__ == '__main__':
    main()
