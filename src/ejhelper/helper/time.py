from typing import Optional

from datetime import datetime, timedelta, timezone
from time import time

# タイムゾーンの生成
JST = timezone(timedelta(hours=+9), 'JST')


def getNow(timezone: Optional[timezone] = None):
    """
        タイムジョンを考慮した現在時間
        Args:
            timezone (timezone): timezone(default: JST)
        Returns:
            str: Currtent datetime in timezone
    """
    if timezone is None:
        timezone = JST
    return datetime.fromtimestamp(currentUnixtime(), timezone)


def getTimestamp():
    """
        タイムジョンを考慮した現在のtimestamp
        Args:
            timezone (timezone): timezone(default: JST)
        Returns:
            int: timestmap millisec
    """
    return int(time() * 1000)


def convertSlot2Unixtime(recorded_date, slot=1):
    minutes = (int(slot) - 1) * 30

    converted_datetime = datetime.strptime(
        str(recorded_date), '%Y%m%d') + timedelta(minutes=minutes)
    return int(converted_datetime.timestamp())

def convertUnixtime2Timestamp(unixtime):
    return datetime.fromtimestamp(unixtime)

def getYear(datetime: Optional[datetime] = None):
    if datetime is None:
        datetime = getNow()
    return str(datetime.year)


def isLeapYear(year):
    """
    閏年の判定
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
        else:
            return True
    return False


def getMonth(datetime: Optional[datetime] = None):
    if datetime is None:
        datetime = getNow()
    return str(datetime.month).zfill(2)


def getDay(datetime: Optional[datetime] = None):
    if datetime is None:
        datetime = getNow()
    return str(datetime.day).zfill(2)


def getTTL(months=0, weeks=0, days=0, hours=0, minutes=0):
    result = datetime.now()
    if months != 0:
        result += timedelta(days=(months * 30))
    if weeks != 0:
        result += timedelta(weeks=weeks)
    if days != 0:
        result += timedelta(days=days)
    if hours != 0:
        result += timedelta(hours=hours)
    if days != 0:
        result += timedelta(minutes=minutes)
    return int(result.timestamp())


def currentUnixtime():
    return int(getTimestamp() / 1000)
