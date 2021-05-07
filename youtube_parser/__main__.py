import asyncio
import logging

from youtube_parser.application import Application
from youtube_parser.config import Config

logger = logging.getLogger(__name__)


async def main():
    logger.info("Start application")

    application = Application(Config())
    try:
        await application.run()
    except Exception as e:
        logger.exception(f"Runtime error: {e}")
    finally:
        logger.info("Stop application")
        await application.stop()


if __name__ == "__main__":
    asyncio.run(main())
