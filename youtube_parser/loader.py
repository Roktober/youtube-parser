import logging
from enum import Enum
from typing import Optional, Callable, Any

import aiohttp
import orjson
from aiohttp import ClientError

logger = logging.getLogger(__name__)


class YoutubeLoader:
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    GOOGLE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(
            self,
            headers: Optional[dict] = None,
            json_dumps: Optional[Callable[[Any], str]] = None,
    ):
        self._headers = headers or self.DEFAULT_HEADERS
        self._json_dumps = json_dumps or orjson.dumps

        self._session = aiohttp.client.ClientSession(
            json_serialize=self._json_dumps,  # type: ignore
            headers=self._headers,
        )

    async def close_session(self):
        await self._session.close()

    async def search(self, params: dict) -> dict:
        logger.info(f'Search with params {params}')
        try:
            data = await self._search(params)
        except ClientError as e:
            logger.exception(f'Search request error: {e}')
            raise e
        return data

    async def _search(self, params: dict) -> dict:
        async with self._session.get(
                self.GOOGLE_SEARCH_URL,
                params=params,
                raise_for_status=True
        ) as req:
            return await req.json()


class SearchOrder(str, Enum):
    Date = 'date'
    Title = 'title'
    Rating = 'rating'
    Relevance = 'relevance'
    ViewCount = 'viewCount'


class SearchType(str, Enum):
    Channel = 'channel'
    Playlist = 'playlist'
    Video = 'video'


class SearchVideoDuration(str, Enum):
    Any = 'any'  # default value
    Long = 'long'  # Only include videos longer than 20 minutes.
    Medium = 'medium'  # Only include videos that are between four and 20 minutes long (inclusive).
    Short = 'short'  # Only include videos that are less than four minutes long.


class SearchParamBuilder(dict):
    """
    see https://developers.google.com/youtube/v3/docs/search/list#parameters for more param
    """

    def __init__(
            self,
            api_key: str,
            part: str = 'snippet'
    ):
        super().__init__()
        self.key(api_key)
        self.part(part)

    def key(self, api_key: str):
        self['key'] = api_key
        return self

    def order(self, order: str):
        self['order'] = order
        return self

    def page_token(self, page_token: str):
        self['pageToken'] = page_token
        return self

    def published_after(self, published_after: str):
        """
        :param published_after: RFC 3339 - zoned time format with T splitter
        """
        self['publishedAfter'] = published_after
        return self

    def published_before(self, published_before: str):
        """
        :param published_before: RFC 3339 - zoned time format with T splitter
        """
        self['publishedBefore'] = published_before
        return self

    def q(self, q: str):
        self['q'] = q
        return self

    def part(self, part: str):
        self['part'] = part
        return self

    def max_results(self, max_results: int):
        if 0 > max_results > 50:
            raise ValueError('maxResults acceptable values are 0 to 50')
        self['maxResults'] = str(max_results)
        return self

    def type(self, type_: str):
        self['type'] = type_
        return self

    def video_duration(self, video_duration: str):
        self['videoDuration'] = video_duration
        return self

    def other_params(self, **kwargs):
        self.update(kwargs)
        return self
