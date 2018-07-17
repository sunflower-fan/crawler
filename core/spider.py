import urllib
import time
import asyncio
import logging

from core.downloader.defaultDownloader import DefaultDownloader
from core.pipeline.defaultPipeline import DefaultPipeline
from core.scheduler.defaultScheduler import DefaultScheduler
from core.processor.processordispatcher import ProcessorDispatcher

LOGGER = logging.getLogger(__name__)


class Spider(object):
    # todo retry, redirect

    def __init__(self, request_list) -> None:
        self.loop = asyncio.get_event_loop()
        self.request_list = request_list
        self.coro_num = 1
        self.page_processor = ProcessorDispatcher()
        self.downloader = DefaultDownloader()
        self.pipeline = DefaultPipeline()
        self.scheduler = DefaultScheduler(self.loop)
        self.root_domains = set()
        self.seen_url = set()
        self.t0 = None
        self.t1 = None

    async def work(self):
        try:
            while True:
                try:
                    rq = await self.scheduler.get()
                    page = await self.downloader.download(rq, self)
                    if page is None:
                        continue
                    self.page_processor.execute(rq, page)
                    await self.scheduler.put_all(page.newRequests)
                    # self.loop.run_in_executor(None, self.pipeline.save_all, page.pageItems)
                    self.pipeline.save_all(page.pageItems)
                    self.scheduler.task_done()
                except asyncio.CancelledError as e:
                    raise e
                except BaseException as e:
                    LOGGER.error(
                        "Working error, url[{}], http status[{}], detail[{}]".format(rq.url, page.http_status, str(e)))
        except asyncio.CancelledError:
            pass

    async def run(self):
        for request in self.request_list:
            self.root_domains.add(urllib.parse.splitport(urllib.parse.urlparse(request.url).netloc)[0])
        self.scheduler.put_all_nowait(self.request_list)
        works = [asyncio.Task(coro=self.work(), loop=self.loop) for _ in range(self.coro_num)]
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
