# ---------------------------------------------------------------------------------------------------------------------
#                   Bot by dima203
#               @TestMyNewTelegramBot
# ---------------------------------------------------------------------------------------------------------------------
from handlers import *
from timer import RepeatedTimer
from player import Player


# Функция лечения игроков
def heal():
    for user_id in DATABASE.get_ids():
        if not DATABASE.get_attr_by_id(user_id, ('is_death',))['is_death']:
            Player(user_id).heal()


# Основной цикл
def main():
    # Создание таймера для лечения игроков
    heal_timer = RepeatedTimer(1, heal)
    try:
        # Запуск цикла
        BOT.polling()

    except Exception as e:
        # Вызов ошибки при наличии
        raise e

    finally:
        # Остановка таймера для лечения игроков
        heal_timer.stop()


if __name__ == '__main__':
    main()
