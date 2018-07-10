from core.downloader.defaultDownloader import DefaultDownloader
from core.pipeline.defaultPipeline import DefaultPipeline
from core.scheduler.defaultScheduler import DefaultScheduler


class Spider(object):

    def __init__(self, page_processor) -> None:
        self.request = None
        self.coroutineNum = 1
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
            if page.newRequests:
                self.scheduler.put(page.newRequests)
            self.pipeline.save(page.pageItems)
            if self.scheduler.qsize() == 0:
                break
