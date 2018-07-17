class Page(object):
    def __init__(self) -> None:
        self.http_status = 200
        self.content = None
        self.newRequests = None
        self.pageItems = None
