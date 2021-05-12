import asyncio
import logging
import signal

from youtube_parser.application import Application
from youtube_parser.config import Config

logger = logging.getLogger(__name__)


async def main():
    logger.info("Start application")
    loop = asyncio.get_running_loop()

    application = Application(Config())
    try:
        await application.run()
        for signal_code in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(
                signal_code, lambda: asyncio.ensure_future(application.stop())
            )
    except Exception as e:
        logger.exception(f"Runtime error: {e}")
        await application.stop()
        logger.info("Stop application")
        raise RuntimeError from e


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    finally:
        loop.close()
