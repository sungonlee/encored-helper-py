from boto3.session import Session
from retry import retry
from uuid import uuid4
from math import ceil
import json
import decimal

from ejhelper2.helper.env import getEnv
from ejhelper2.helper.logging import getLogger

logger = getLogger(__name__)


class S3:

    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

        profile = getEnv('PROFILE', None)
        if profile is None:
            session = Session()
        else:
            session = Session(profile_name=profile)
        self.s3 = session.resource('s3')
        self.meta = self.s3.meta
        self.bucket = self.s3.Bucket(self.bucket_name)
        self.objects = self.bucket.objects

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def Object(self, key):
        return self.bucket.Object(key)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def object_put(self, key, data):
        return self.bucket.Object(key).put(Body=json.dumps(data, ensure_ascii=False))

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def object_get(self, key):
        response = self.bucket.Object(key).get()
        body = response['Body'].read()
        return json.loads(body.decode('utf-8'))

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def upload_file(
            self,
            file_path,
            key,
            ExtraArgs=None,
            Callback=None,
            Config=None):
        return self.bucket.upload_file(file_path, key)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def put_fileobj(
            self,
            fileobj,
            key,
            ExtraArgs=None,
            Callback=None,
            Config=None):
        return self.put(fileobj, key)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def upload_fileobj(
            self,
            fileobj,
            key,
            ExtraArgs=None,
            Callback=None,
            Config=None):
        return self.bucket.upload_fileobj(fileobj, key)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def put_object(
            self,
            key,
            data,
            ExtraArgs=None,
            Callback=None,
            Config=None):
        return self.bucket.put_object(
            Key=key, Body=json.dumps(
                data, cls=DecimalEncoder))

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def download_file(self, key, file_path):
        return self.bucket.download_file(key, file_path)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def head_object(self, key, **kwargs):
        """
        ヘッダー情報取得

        response sample

        {
        'AcceptRanges': 'bytes',
        'ContentLength': 71352,
        'ContentType': 'binary/octet-stream',
        'ETag': '"6dc2578a1487ea1ed7...665781a0"',
        'LastModified': datetime.datetime(20...o=tzutc()),
        'Metadata': {
        },
        'ResponseMetadata': {
            'HTTPHeaders': {
            ...
            },
            'HTTPStatusCode': 200,
            'HostId': 'XH+GK5Oq9HGU54VtmfK...lt+9RcLU=',
            'RequestId': 'E32D331143CF3C12',
            'RetryAttempts': 0
        }
        }
        """
        result = None
        try:
            result = self.s3.meta.client.head_object(
                Bucket=self.bucket_name, Key=key, **kwargs)
        except Exception as e:
            logger.debug(e.args)
            result = None
        return result

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def copy(self, copy_source, otherbucket, otherkey):
        """
        copy_source = {
            'Bucket': 'mybucket',
            'Key': 'mykey'
        }
        """
        return self.meta.client.copy(copy_source, otherbucket, otherkey)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def delete_object(self, key, **kwargs):
        """
        ヘッダー情報取得

        response sample

        {
            'DeleteMarker': True|False,
            'VersionId': 'string',
            'RequestCharged': 'requester'
        }
        """
        return self.s3.meta.client.delete_object(
            Bucket=self.bucket_name, Key=key, **kwargs)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def decimalEncoder(o):
    if isinstance(o, decimal.Decimal):
        if o % 1 > 0:
            return float(o)
        else:
            return int(o)
    return o


def create_s3_store(s3_bucket: str, prefix: str, values, limit: int = None):
    """[リストを分割してS3に格納]通知情報連携様

    Args:
        s3_bucket (str): [連携ファイルお記載]
        prefix (str): [S3keyのprefix]
        values (list): [分割対象データリスト]
        limit (int, optional): [分割時１つの最大数]. Defaults to None.

    Returns:
        [list]: [S3Keyリスト]0件の場合は [ None ]を返す ※ step funtionsで例外処理せず、通常成功させるため
    """
    result = []
    upload_bucket = S3(s3_bucket)

    # 配列分割
    len_values = len(values)
    if limit is None:
        limit = len_values

    if len_values == 0:
        split_list = [None]
    else:
        n = int((len_values - 1) / limit) + 1  # limitいないにすつための分割数
        page = ceil(len_values / n)
        split_list = [values[idx:idx + page]
                      for idx in range(0, len_values, page)]

    key_prefix = f'{prefix}/{str(uuid4())}'
    for index, item in enumerate(split_list):
        key = f'{key_prefix}/{index}'
        upload_bucket.put_object(key, item)
        result.append(key)
    return result
