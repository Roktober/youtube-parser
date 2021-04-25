import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal, List

from youtube_parser.utils import from_iso_8601

logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(
    "([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"
)


@dataclass()
class YoutubeSearchItem:
    video_id: str
    channel_id: str
    title: str
    description: str
    channel_title: str
    published_at: datetime
    live_broadcast_content: Optional[Literal['live', 'upcoming']]


@dataclass()
class YoutubeSearchResponse:
    youtube_search_items: List[YoutubeSearchItem]
    next_page_token: Optional[str]
    prev_page_token: Optional[str]
    total_result: int
    result_kind: str


def extract_youtube_search_response(response: dict) -> YoutubeSearchResponse:
    next_page_token = extract_next_page_token_from_response(response)
    prev_page_token = extract_prev_page_token_from_response(response)
    total_result = extract_total_result_from_response(response)
    result_kind = extract_result_kind_from_response(response)

    if result_kind != 'youtube#searchListResponse':
        raise ValueError(f'Unexpected result kind {result_kind}')

    logger.info(f'Next page token {next_page_token}')
    logger.info(f'Prev page token {prev_page_token}')
    logger.info(f'Total result {total_result}')

    items: List[YoutubeSearchItem] = []
    for item in response['items']:
        kind = item['kind']
        if kind == 'youtube#searchResult':
            video_id = extract_video_id_from_item(item)
            channel_id = extract_channel_id_from_item_snippet(item)
            title = extract_title_from_item_snippet(item)
            description = extract_description_from_item_snippet(item)
            channel_title = extract_channel_title_from_item_snippet(item)
            published_at = extract_published_at_from_item_snippet(item)
            live_broadcast_content = extract_live_broadcast_content_from_item_snippet(item)

            extracted_item = YoutubeSearchItem(
                video_id=video_id,
                published_at=published_at,
                channel_id=channel_id,
                channel_title=channel_title,
                title=title,
                description=description,
                live_broadcast_content=live_broadcast_content,
            )
            items.append(extracted_item)
        else:
            logger.error(f'Unexpected item kind {kind}')
    result = YoutubeSearchResponse(
        youtube_search_items=items,
        next_page_token=next_page_token,
        prev_page_token=prev_page_token,
        result_kind=result_kind,
        total_result=total_result,
    )
    return result


def extract_video_id_from_item(item: dict) -> str:
    return item['id']['videoId']


def extract_published_at_from_item_snippet(item: dict) -> datetime:
    return from_iso_8601(item['snippet']['publishedAt'])


def extract_channel_id_from_item_snippet(item: dict) -> str:
    return item['snippet']['channelId']


def extract_channel_title_from_item_snippet(item: dict) -> str:
    return item['snippet']['channelTitle']


def extract_title_from_item_snippet(item: dict) -> str:
    return item['snippet']['title']


def extract_description_from_item_snippet(item: dict) -> str:
    return item['snippet']['description']


def extract_live_broadcast_content_from_item_snippet(item: dict) -> Optional[Literal['live', 'upcoming']]:
    lvc = item['snippet']['liveBroadcastContent']
    if lvc == 'none':
        return None
    else:
        if lvc != 'live' and lvc != 'upcoming':
            raise ValueError(f'liveBroadcastContent has unexpected value: {lvc}')
    return lvc


def extract_next_page_token_from_response(response: dict) -> Optional[str]:
    return response.get('nextPageToken', None)


def extract_prev_page_token_from_response(response: dict) -> Optional[str]:
    return response.get('prevPageToken', None)


def extract_total_result_from_response(response: dict) -> int:
    return int(response['pageInfo']['totalResults'])


def extract_result_kind_from_response(response: dict) -> str:
    return response['kind']


def parse_email(string: str) -> List[str]:
    return re.findall(EMAIL_REGEX, string)
