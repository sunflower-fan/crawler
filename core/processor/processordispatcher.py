class ProcessorDispatcher(object):
    def execute(self, request, page):
        request.processor(page)
