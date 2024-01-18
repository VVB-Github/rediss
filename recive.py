import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

async def on_message(message: AbstractIncomingMessage) -> None:
    print(" [x] Received message %r" % message.routing_key)
    
async def main() -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("start_cashe")
        queue2 = await channel.declare_queue("cashe_created")
        await queue.consume(on_message, no_ack=True)
        await queue2.consume(on_message, no_ack=True)
        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()
        
        
if __name__ == "__main__":
    asyncio.run(main())