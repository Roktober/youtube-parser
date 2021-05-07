import asyncio
import logging

from youtube_parser.parser import Parser
from youtube_parser.cache import RedisCache
from youtube_parser.config import Config
from youtube_parser.loader import (
    YoutubeLoader,
    SearchParamBuilder,
    SearchOrder,
    SearchType,
    SearchVideoDuration,
)
from youtube_parser.metrics import Metrics

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, config: Config):
        self._config = config
        self._metrics = Metrics()
        self._cache = RedisCache(db=1)
        self._youtube_loader = YoutubeLoader()

    async def run(self):
        logger.info("Start metrics")
        self._metrics.start_server()

        params = (
            SearchParamBuilder(api_key=self._config.youtube_parser.api_key)
            .q("lofi hip-hop")
            .order(SearchOrder.Date.value)
            .type(SearchType.Video.value)
            .video_duration(SearchVideoDuration.Long.value)
            .max_results(50)
        )

        parser = Parser(
            loader=self._youtube_loader,
            metrics=self._metrics,
            email_cache=self._cache,
            search_param=params,
        )

        await parser.parse()

    async def stop(self):
        await self._youtube_loader.close_session()
