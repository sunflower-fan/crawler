class ProcessorDispatcher(object):
    def execute(self, request, page):
        request.function(page)
