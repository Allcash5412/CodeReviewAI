import logging.config

from pathlib import Path
from typing import Dict

from pydantic import Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

default_config: Dict = SettingsConfigDict(env_file=BASE_DIR / '.env', extra='ignore')

class DefaultModelConfig:
    model_config: Dict = default_config


class GlobalSettings(BaseSettings, DefaultModelConfig):
    start_setting: str = Field(alias='START_SETTING')
    logger_config: Dict = {}

    @field_validator('logger_config')
    def get_logger_config(cls, v, info: FieldValidationInfo):
        logger_config = cls.get_logger_config_by_setting(info.data['start_setting'])
        return logger_config

    @classmethod
    def get_logger_config_by_setting(cls, start_setting: str) -> Dict:
        if start_setting == 'PRODUCTION':
            LOGGER_CONFIG = {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'default': {
                        'format': '%(levelname)s: %(message)s'
                    },
                    'detailed': {
                        'format': '[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s',
                        'datefmt': '%Y-%m-%dT%H:%M:%S%z'
                    }
                },
                'handlers': {
                    'console': {
                        'level': 'WARNING',
                        'class': 'logging.StreamHandler',
                        'formatter': 'detailed'
                    },
                    'file': {
                        'level': 'DEBUG',
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'filename': 'app.log',
                        'when': 'W0',
                        'utc': True,
                        'formatter': 'detailed',
                    },
                },
                'loggers': {
                    'uvicorn': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'uvicorn.error': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'uvicorn.access': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'app': {
                        'level': 'DEBUG',
                        'handlers': ['console', 'file'],
                        'propagate': False
                    },
                },
                'root': {
                    'level': 'WARNING',
                    'handlers': ['console']
                }
            }
        else:
            LOGGER_CONFIG = {
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'default': {
                        'format': '%(levelname)s: %(message)s'
                    },
                    'detailed': {
                        'format': '[%(levelname)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s',
                        'datefmt': '%Y-%m-%dT%H:%M:%S%z'
                    }
                },
                'handlers': {
                    'console': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                        'formatter': 'detailed'
                    },
                    'file': {
                        'level': 'INFO',
                        'class': 'logging.handlers.TimedRotatingFileHandler',
                        'filename': 'app.log',
                        'when': 'W0',
                        'utc': True,
                        'formatter': 'detailed',
                    },
                },
                'loggers': {
                    'uvicorn': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'uvicorn.error': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'uvicorn.access': {
                        'level': 'INFO',
                        'handlers': ['console'],
                        'propagate': False
                    },
                    'app': {
                        'level': 'DEBUG',
                        'handlers': ['console', 'file'],
                        'propagate': False
                    },
                },
                'root': {
                    'level': 'WARNING',
                    'handlers': ['console']
                }
            }

        return LOGGER_CONFIG


class ExternalAPI(BaseSettings, DefaultModelConfig):
    github_api_token: str = Field(alias='GITHUB_API_TOKEN')
    ai_chat_api_url: str = Field(alias='AI_CHAT_API_URL')


class Settings(BaseSettings):
    global_settings: GlobalSettings = GlobalSettings()
    external_api: ExternalAPI = ExternalAPI()


settings = Settings()
logging.config.dictConfig(settings.global_settings.logger_config)
