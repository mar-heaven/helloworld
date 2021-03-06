import logging
from helloworld.db.database import close_mongo_conn, create_mongo_conn


async def connect_db() -> None:
    logging.info("connect_db starting")
    create_mongo_conn()
    logging.info("connect_db finished")


async def close_db() -> None:
    logging.info("close_db starting")
    close_mongo_conn()

    logging.info("close_db finished")


async def start_up():
    await connect_db()


async def shutdown():
    await close_db()
