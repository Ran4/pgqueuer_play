from dotenv import load_dotenv

load_dotenv()
import asyncio
import os
import sys

import asyncpg
from PgQueuer.models import Job
from PgQueuer.qm import QueueManager

DATABASE_DSN = os.environ["DATABASE_DSN"]


async def get_queue_manager():
    pool = await asyncpg.create_pool(
        min_size=2,
        dsn=DATABASE_DSN,
    )
    assert pool
    return QueueManager(pool=pool)


async def sender(qm: QueueManager):
    for n in range(10):
        await qm.queries.enqueue("fetch", f"this is from me: {n}".encode())


async def receiver(qm: QueueManager):
    @qm.entrypoint("fetch")
    async def process_message(job: Job) -> None:
        breakpoint()
        print(f"Processed message: {job}")

    _ = process_message
    await qm.run()


async def main() -> None:
    qm = await get_queue_manager()

    try:
        command = sys.argv[1]
    except IndexError:
        print("Usage: PROGRAM sender|receiver")
        return

    if command == "sender":
        await sender(qm)

    elif command == "receiver":
        await receiver(qm)


if __name__ == "__main__":
    asyncio.run(main())
