from dotenv import load_dotenv
from pydantic import BaseSettings, Field
import json
import os

from .logging import logger

from pathlib import Path


ENV_PREFIX = 'battleship_api'


class Settings(BaseSettings):
    host: str = Field('127.0.0.1')
    port: int = Field(80)
    debug: bool = Field(True)

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = f'{ENV_PREFIX}_'


def get_settings(json_path: Path | None = None, **settings_set) -> Settings:
    """
    Function that creates and returns an settings object from (higher position
    means higher piority):
        - Json configuration file available at given `json_path`
        - keyword parameters passed to this function
        - environment variables

    Params:
        - json_path [Optional] - Filepath to json configuration file.
            - If not provided, by default function tries to get path from
              `{battleship_api.core.settings.ENV_PREFIX}_config_path`
              enviroment variable.
            - If is it not possible to get path from both parameter and
              enviroment variable function skips attemp of reading
              configuration file.

        - **settings_set - Keyword parameters overwriting settings defined by
          the enviroment variables.
            - Can be overwrited by settings from json configuration file.

    Returns:
        Settings object instance
    """
    if not json_path:
        load_dotenv()
        json_path = os.getenv(f'{ENV_PREFIX}_config_path')
    if json_path:
        try:
            config = json.load(open(json_path, encoding='utf-8'))
        except FileNotFoundError:
            logger.warning(
                f"Config file `{json_path}` could not be found.")
        except json.decoder.JSONDecodeError:
            logger.warning(
                f"Config file `{json_path}` could not be decoded properly.")
        else:
            settings_set |= config
    return Settings(**settings_set)
