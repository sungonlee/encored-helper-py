from logging import getLogger as getLoggerOrg, StreamHandler, Formatter, DEBUG, INFO
from ejhelper2.helper.env import getEnv, DEBUG_MODE, LOG_MODE, PROJECT_PREFIX


def getLogger(name):
    logLevel = DEBUG
    if getEnv(DEBUG_MODE) == '0':
        logLevel = INFO
    else:
        # PROJECT_PREFIXは毎回取得（Global定義禁止）
        PJ_PREFIX: str = getEnv(PROJECT_PREFIX)  # （Global定義禁止）
        name = f'{name}[{PJ_PREFIX}]'
    logger = getLoggerOrg(name)

    if getEnv(LOG_MODE) == 'stream':
        handler = StreamHandler()
        formatter = Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logLevel)
        logger.addHandler(handler)

    logger.setLevel(logLevel)
    return logger
