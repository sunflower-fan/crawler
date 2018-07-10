from core.downloader import DefaultDownloader
from core.pipeline import DefaultPipeline
from core.scheduler import DefaultScheduler


class Spider(object):

    def __init__(self, page_processor) -> None:
        self.request
        self.coroutineNum
        self.pageProcessor = page_processor
        self.downloader = DefaultDownloader()
        self.pipeline = DefaultPipeline()
        self.scheduler = DefaultScheduler()

    def start(self):
        self.scheduler.put(self.request)
        while True:
            rq = self.scheduler.get()
            page = self.downloader.download(rq)
            self.pageProcessor.process(page)
            self.scheduler.put(page.newRequests)
            self.pipeline.save(page.pageItems)
            if self.scheduler.qsize() == 0:
                break
