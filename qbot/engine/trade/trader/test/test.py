import aioredis
import asyncio


async def reader(message):
    print(f"in reader: {message}, type={type(message)}")


async def monitor1(pb: aioredis.client.PubSub):
    async for msg in pb.listen():
        print(f"in monitor1: {msg}, type={type(msg)}")
        asyncio.create_task(reader(msg))
        if msg['type'] == 'punsubscribe':
            print('quit monitor1')
            break


async def main():
    redis = await aioredis.from_url("redis://192.168.123.142", decode_responses=True)
    pubsub1 = redis.pubsub()
    pubsub2 = redis.pubsub()
    await pubsub1.psubscribe('channel:*')
    await pubsub2.psubscribe('channel*')
    await redis.publish("channel:1", "1")
    await redis.publish("channel:2", "6")
    await redis.publish("channel:3", "3")
    await pubsub1.punsubscribe()
    await pubsub2.punsubscribe()
    loop = asyncio.get_running_loop()
    asyncio.run_coroutine_threadsafe(monitor1(pubsub1), loop)
    asyncio.run_coroutine_threadsafe(monitor1(pubsub2), loop)
    # await asyncio.gather(monitor1(pubsub1), monitor1(pubsub2))
    # await pubsub2.run()
    print('main done!')

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass

