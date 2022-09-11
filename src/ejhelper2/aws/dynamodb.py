from boto3.session import Session
from retry import retry
from typing import Any

from ejhelper2.helper.env import getEnv, EXEC_ENV, PROJECT_PREFIX
from ejhelper2.helper.logging import getLogger

env: str = getEnv(EXEC_ENV)

logger = getLogger(__name__)


class DynamoDBTableV2:

    tablename: str = ''
    tablename_org: str = ''
    table: dict[str, Any] = dict()

    def __init__(self, tablename, **kwargs):
        self.init(tablename, **kwargs)

    def init(self, tablename, **kwargs):
        # PROJECT_PREFIXは毎回取得
        PJ_PREFIX: str = getEnv(PROJECT_PREFIX)  # （Global定義禁止）

        env_tablename: str = getEnv(
            f'DYNAMODB_TABLENAME__{tablename}', tablename)
        if tablename == env_tablename:
            local_tablename = f'{env}{PJ_PREFIX}{tablename}'
        else:
            local_tablename = env_tablename
            kwargs['aws_access_key_id'] = getEnv(
                f'DYNAMODB_ACCESS_KEY_ID__{tablename}')
            kwargs['aws_secret_access_key'] = getEnv(
                f'DYNAMODB_SECRET_ACCESS_KEY__{tablename}')
            logger.info(f'use env table name : {env_tablename}')

        profile = getEnv(
            f'DYNAMODB_PROFILE__{tablename}', getEnv('PROFILE', None))
        if profile is None:
            session = Session()
        else:
            session = Session(profile_name=profile)
        self.dynamodb = session.resource('dynamodb', **kwargs)

        self.table[PJ_PREFIX] = self.dynamodb.Table(local_tablename)
        self.tablename_org = tablename
        self.tablename = local_tablename

    def _check_project(self):
        """同一インスタンで異なるプロジェクトがよばれた時
        """
        # PROJECT_PREFIXは毎回取得
        PJ_PREFIX: str = getEnv(PROJECT_PREFIX)  # （Global定義禁止）
        if PJ_PREFIX not in self.table:
            logger.warn(
                f'_check_project before: tablename:{self.tablename}, current PJ_PREFIX={PJ_PREFIX}')
            option: Any = {}
            self.init(self.tablename_org, **option)
        return self.table[PJ_PREFIX]

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def scan(self, **kwargs):
        return self._check_project().scan(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def query(self, **kwargs):
        return self._check_project().query(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def batch_get_item(self, **kwargs):
        """

        sample code>>

            response = dynamodb.batch_get_item(
                RequestItems={
                    table_name: {
                        'Keys': [
                        {'id_device':'ras0002', 'timestamp':"20180122082200"},
                        {'id_device':'ras0002', 'timestamp':"20180122082300"},
                        {'id_device':'ras0003', 'timestamp':"20180122082300"}
                            ]
                        }
                })
            #
            display_proc(response['Responses'][table_name])
            #
        """
        return self.dynamodb.batch_get_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def update_item(self, **kwargs):
        return self._check_project().update_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def put_item(self, **kwargs):
        return self._check_project().put_item(**kwargs)

    @retry(tries=2, delay=1, backoff=1, logger=logger)
    def get_item(self, **kwargs):
        return self._check_project().get_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def delete_item(self, **kwargs):
        return self._check_project().delete_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def batch_writer(self, **kwargs):
        """
        overwrite_by_pkeys=['partition_key', 'sort_key']
        """
        return self._check_project().batch_writer(**kwargs)
