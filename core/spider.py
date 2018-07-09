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
        self.scheduler.push(self.request)
        while True:
            todo_request = self.scheduler.poll()
            # download page
            self.pageProcessor.process(todo_request)
