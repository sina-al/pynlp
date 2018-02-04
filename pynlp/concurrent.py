from threading import Thread
from queue import Queue


class Worker(Thread):

    def __init__(self, tasks):
        super().__init__(daemon=True)
        self.tasks = tasks

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as ex:  # TODO: Log
                print(ex)
            self.tasks.task_done()


class ThreadPool:

    def __init__(self, n_threads):
        self.tasks = Queue(n_threads)
        for _ in range(n_threads):
            Worker(self.tasks).start()

    def put(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def join(self):
        self.tasks.join()
