class DefaultPipeline(object):
    def save(self, item):
        if item:
            print(item)

    def save_all(self, items):
        if items:
            for item in items:
                self.save(item)
