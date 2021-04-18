import asyncio
import logging
from datetime import datetime

from dateutil.tz import UTC

from extractor import extract_youtube_search_response, parse_email
from loader import SearchOrder, SearchType, SearchVideoDuration, SearchParamBuilder, YoutubeLoader
from utils import to_rfc_339_time

logger = logging.getLogger(__name__)


async def main():
    with open('creds', 'r') as f:
        key = f.read()

    params = SearchParamBuilder(api_key=key). \
        q('lofi hip-hop'). \
        order(SearchOrder.Rating.value). \
        type(SearchType.Video.value). \
        video_duration(SearchVideoDuration.Long.value). \
        max_results(50)
        # published_after(to_rfc_339_time(datetime.now(tz=UTC))). \

    loader = YoutubeLoader()

    # Page token example
    for i in range(10):
        data = extract_youtube_search_response(await loader.search(params))

        for item in data.youtube_search_items:
            emails = parse_email(item.description)
            if emails:
                print(emails)
            print(emails)

        params.page_token(data.next_page_token)

    await loader.close_session()

asyncio.run(main())
