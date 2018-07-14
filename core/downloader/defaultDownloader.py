from core.page import Page

import aiohttp


class DefaultDownloader(object):

    def __init__(self) -> None:
        super().__init__()

    async def download(self, rq):
        async with aiohttp.request(method='GET', url=rq.url, headers=rq.headers) as r:
            content = await r.text()
            page = Page()
            page.content = content
            return page
