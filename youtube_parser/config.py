import logging

from pydantic import BaseSettings, Field


class YoutubeParserConfig(BaseSettings):
    """
    Parser configuration
    """
    api_key: str = Field(
        description='YouTube api key see: https://developers.google.com/youtube/v3/getting-started'
    )

    class Config:
        env_prefix = 'YOUTUBE_'


class Logging:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level='INFO')


class Config:
    youtube_parser = YoutubeParserConfig()
    logging = Logging()
