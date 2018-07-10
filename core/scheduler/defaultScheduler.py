from queue import Queue


class DefaultScheduler(object):

    def __init__(self) -> None:
        self.queue = Queue()

    def put(self, request):
        self.queue.put(request)

    def get(self):
        return self.queue.get()

    def qsize(self):
        return self.queue.qsize()
