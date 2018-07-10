from queue import Queue


class DefaultScheduler(object):

    def __init__(self) -> None:
        self.queue = Queue.queue()

    def put(self, request):
        self.queue.put(request)

    def get(self):
        return self.queue.get()

    def qsize(self):
        self.queue.qsize()
