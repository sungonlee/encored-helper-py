from os import environ
from typing import Optional

LOG_MODE = 'LOG_MODE'
DEBUG_MODE = 'DEBUG_MODE'
EXEC_ENV = 'EXEC_ENV'
AWS_PREFIX = 'AWS_PREFIX'
PROJECT_PREFIX = 'PJ_PREFIX'  # 各プロジェクト（パッケージの）prefix
ACCESS_KEY_ID = 'ACCESS_KEY_ID'
SECRET_ACCESS_KEY = 'SECRET_ACCESS_KEY'


# 環境変数保存用 dict
pj_env_dict: dict[str, Optional[str]] = dict()


def getEnvOrg(key, default: Optional[str] = None):
    value = None
    # DefaultValue
    if key == DEBUG_MODE:
        value = environ.get(key, '0')
    elif key == EXEC_ENV or key == AWS_PREFIX:
        value = environ.get(key, 'dev')
    else:
        value = environ.get(key, default)
    return value


def getEnv(key, default: Optional[str] = None):
    """各プロジェクトに合わせた設定を取得する
       ex) HOST_NAME → Derms_HOST_NAME 例外キーワードPJ_PREFIX
    Args:
        key (_type_): 環境変数キー
        default (Optional[str], optional): _description_. Defaults to None.

    Returns:
        _type_: 環境変数設定値
    """

    # 例外キーワード
    if key == PROJECT_PREFIX:
        return environ.get(PROJECT_PREFIX)

    pj_prifx: str = environ.get(PROJECT_PREFIX, '')
    pj_key: str = f'{pj_prifx}_{key}'

    if pj_key not in pj_env_dict:
        value = None

        value = environ.get(pj_key, None)
        if value is None:
            # 定義がない場合は、input keyで検索
            value = getEnvOrg(key, default)
        pj_env_dict[pj_key] = value

    return pj_env_dict[pj_key]


def setEnv(key, value):
    environ[key] = value
    if key in pj_env_dict:
        del pj_env_dict[key]
