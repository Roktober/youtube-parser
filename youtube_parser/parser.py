import logging
from typing import Optional, Set, List

from youtube_parser.cache import RedisCache
from youtube_parser.extractor import (
    extract_youtube_search_response,
    YoutubeSearchResponse,
    parse_email,
)
from youtube_parser.loader import YoutubeLoader
from youtube_parser.metrics import Metrics

logger = logging.getLogger(__name__)


class Parser:
    def __init__(
        self,
        loader: YoutubeLoader,
        email_cache: RedisCache,
        metrics: Metrics,
        search_param: dict,
    ):
        self._email_cache = email_cache
        self._loader = loader
        self._metrics = metrics
        self._search_param = search_param

    async def parse(self) -> None:
        data = await self._do_query()
        if not data:
            return None
        emails = _parse_emails(data)
        unique_emails = self._get_unique_emails(emails)
        if unique_emails:
            self._save_emails(unique_emails)

        self._metrics.emails_found.inc(len(emails))
        self._metrics.unique_emails_found.inc(len(unique_emails))
        self._metrics.video_processed.inc(len(data.youtube_search_items))

    async def _do_query(self) -> Optional[YoutubeSearchResponse]:
        try:
            data = await self._loader.search(self._search_param)
            return _parse_response(data)
        except Exception as exc:
            logger.exception(f"Do query error: {exc}")
            return None

    def _get_unique_emails(self, emails: List[str]) -> List[str]:
        unique_emails = []
        if emails:
            unique_emails = self._email_cache.filter(emails)
            logger.info(f"Found {len(unique_emails)} unique emails: {unique_emails}")
        return unique_emails

    def _save_emails(self, emails: List[str]) -> None:
        self._email_cache.mset({u_email: "" for u_email in emails})


def _parse_emails(parsed_response: YoutubeSearchResponse) -> List[str]:
    emails: Set[str] = set()
    for item in parsed_response.youtube_search_items:
        parsed_emails = parse_email(item.description)
        for e in parsed_emails:
            emails.add(e[0])
    logger.info(f"Found {len(emails)} emails: {emails}")
    return list(emails)


def _parse_response(response: dict) -> Optional[YoutubeSearchResponse]:
    try:
        return extract_youtube_search_response(response)
    except (ValueError, KeyError) as exc:
        logger.exception(f"Error while extract data: {exc}")
        return None
