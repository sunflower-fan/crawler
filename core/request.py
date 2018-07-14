class Request(object):

    def __init__(self, url, processor, headers) -> None:
        self.url = url
        self.headers = headers
        self.processor = processor
