from asyncio import Queue


class DefaultScheduler(object):

    def __init__(self, loop) -> None:
        self.queue = Queue(loop=loop)

    async def put(self, request):
        if request:
            await self.queue.put(request)

    async def put_all(self, request_list):
        if request_list:
            for request in request_list:
                await self.queue.put(request)

    def put_all_nowait(self, request_list):
        if request_list:
            for request in request_list:
                self.queue.put_nowait(request)

    async def get(self):
        t = await self.queue.get()
        return t

    def qsize(self):
        return self.queue.qsize()

    def task_done(self):
        self.queue.task_done()

    async def join(self):
        await self.queue.join()
