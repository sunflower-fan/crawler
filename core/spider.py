from core.downloader.defaultDownloader import DefaultDownloader
from core.pipeline.defaultPipeline import DefaultPipeline
from core.scheduler.defaultScheduler import DefaultScheduler
from core.processor.processordispatcher import ProcessorDispatcher

import time
import asyncio


class Spider(object):

    def __init__(self, request_list) -> None:
        self.loop = asyncio.get_event_loop()
        self.requestList = request_list
        self.coroNum = 1
        self.pageProcessor = ProcessorDispatcher()
        self.downloader = DefaultDownloader()
        self.pipeline = DefaultPipeline()
        self.scheduler = DefaultScheduler(self.loop)
        self.t0 = None
        self.t1 = None

    async def work(self):
        try:
            while True:
                rq = await self.scheduler.get()
                page = await self.downloader.download(rq)
                self.pageProcessor.execute(rq, page)
                await self.scheduler.put_all(page.newRequests)
                # self.loop.run_in_executor(None, self.pipeline.save_all, page.pageItems)
                self.pipeline.save_all(page.pageItems)
                self.scheduler.task_done()
        except asyncio.CancelledError:
            pass

    async def run(self):
        self.scheduler.put_all_nowait(self.requestList)
        works = [asyncio.Task(coro=self.work(), loop=self.loop) for _ in range(self.coroNum)]
        self.t0 = time.time()
        await self.scheduler.join()
        self.t1 = time.time()
        for work in works:
            work.cancel()

    def start(self):
        self.loop.run_until_complete(self.run())
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()
