from threading import Timer


# Класс таймера
class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    # Метод для выполнения функции по таймеру и его перезапуск
    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    # Метод для запуска таймера
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    # Метод для остановки таймера
    def stop(self):
        self._timer.cancel()
        self.is_running = False
