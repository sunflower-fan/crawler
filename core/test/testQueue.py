import asyncio


async def main(loop, q):
    print(q.qsize())
    await q.put("sfsdfasd")
    print(q.qsize())
    get = await q.get()
    print(get)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    q = asyncio.Queue(loop=loop)
    loop.run_until_complete(main(loop, q))
    loop.close()
