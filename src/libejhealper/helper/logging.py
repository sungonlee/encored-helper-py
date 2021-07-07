from logging import getLogger as getLoggerOrg, StreamHandler, Formatter, DEBUG, INFO
from libejhealper.helper.env import getEnv, DEBUG_MODE, LOG_MODE


def getLogger(name):
    logLevel = DEBUG
    if getEnv(DEBUG_MODE) == '0':
        logLevel = INFO
    logger = getLoggerOrg(name)

    if getEnv(LOG_MODE) == 'stream':
        handler = StreamHandler()
        formatter = Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        handler.setLevel(logLevel)
        logger.addHandler(handler)

    logger.setLevel(logLevel)
    return logger
