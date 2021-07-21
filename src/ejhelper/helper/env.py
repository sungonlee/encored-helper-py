from os import environ
from typing import Optional

LOG_MODE = 'LOG_MODE'
DEBUG_MODE = 'DEBUG_MODE'
EXEC_ENV = 'EXEC_ENV'
AWS_PREFIX = 'AWS_PREFIX'
ACCESS_KEY_ID = 'ACCESS_KEY_ID'
SECRET_ACCESS_KEY = 'SECRET_ACCESS_KEY'

# 環境変数保存用 dict
env_dict = {}


def getEnv(key, default: Optional[str] = None):
    if key not in env_dict:
        value = None
        # DefaultValue
        if key == DEBUG_MODE:
            value = environ.get(key, '0')
        elif key == EXEC_ENV or key == AWS_PREFIX:
            value = environ.get(key, 'dev')
        else:
            value = environ.get(key, default)

        env_dict[key] = value

    return env_dict[key]

