import aiohttp
import logging
from core.page import Page

LOGGER = logging.getLogger(__name__)


class DefaultDownloader(object):

    def __init__(self) -> None:
        super().__init__()

    async def download(self, rq, spider):
        if rq.url in spider.seen_url:
            return None
        retry_count = 0
        while retry_count <= spider.max_retry:
            try:
                async with aiohttp.request(method='GET', url=rq.url, headers=rq.headers) as r:
                    status = r.status
                    if status is not 200:
                        raise SystemError("Download Page Failed, http status[{}]".format(status))
                    content = await r.text()
                    page = Page()
                    page.http_status = status
                    page.content = content
                    spider.seen_url.add(rq.url)
                    return page
            except BaseException as e:
                if retry_count >= spider.max_retry:
                    raise e
                LOGGER.info('try [%r] for [%r] http status [%r] raised [%r]', retry_count, rq.url, status, e)
            retry_count += 1
