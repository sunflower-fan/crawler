from core.downloader.defaultDownloader import DefaultDownloader
from core.pipeline.defaultPipeline import DefaultPipeline
from core.scheduler.defaultScheduler import DefaultScheduler
from core.processor.processordispatcher import ProcessorDispatcher

import time


class Spider(object):

    def __init__(self, request_list) -> None:
        self.requestList = request_list
        self.coroutineNum = 1
        self.pageProcessor = ProcessorDispatcher()
        self.downloader = DefaultDownloader()
        self.pipeline = DefaultPipeline()
        self.scheduler = DefaultScheduler()

    def start(self):
        start = time.time()
        self.scheduler.put_all(self.requestList)
        while True:
            rq = self.scheduler.get()
            page = self.downloader.download(rq)
            self.pageProcessor.execute(rq, page)
            if page.newRequests:
                for r in page.newRequests:
                    self.scheduler.put(r)
            if page.pageItems:
                self.pipeline.save(page.pageItems)
            if self.scheduler.qsize() == 0:
                break
        print("Elapsed time: {}".format(time.time() - start))

