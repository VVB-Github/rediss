'''
кеш в редиске храним
работают 2 экземпляра одного и того же сервиса, используют один и тот же кеш. 
Построение кеша занимает время, кеш строится сервисом при старте. 
Если один сервис строит кеш, то второй ждет. Кеш в виде json. 
'''

import redis, asyncio
from aio_pika import Message, connect
import time

async def build_cache():
    cache_data = {'key1':'value1', 'key2':'value2','key3':'value3', 'key4':'value4'}
    r = redis.Redis(host="localhost", port=6379)
    time.sleep(len(cache_data))
    for key, value in cache_data.items():
        r.hset('hash_key',key,value)
    r.close()


async def main() -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue('start_cashe')
        await channel.default_exchange.publish(
            Message(b'start_cashe'),
            routing_key = queue.name,
        )
        print('[x] Cashe creation started')
        
        await build_cache()

        queue2 = await channel.declare_queue('cashe_created')
        await channel.default_exchange.publish(
            Message(b'cashe_ctreated'),
            routing_key = queue2.name,
        )
        print('[x] Cashe creation ended')
    
    await connection.close()


if __name__=='__main__':
    asyncio.run(main())