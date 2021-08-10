from boto3.session import Session
from retry import retry

from ejhelper.helper.env import getEnv, EXEC_ENV
from ejhelper.helper.logging import getLogger

env: str = getEnv(EXEC_ENV)

logger = getLogger(__name__)


class DynamoDBTable:

    tablename: str = ''

    def __init__(self, tablename, **kwargs):

        env_tablename: str = getEnv(
            f'DY_{tablename}_TABLE_NAME', tablename)
        if tablename == env_tablename:
            local_tablename = f'{env}{self.tablename}'
        else:
            local_tablename = env_tablename
            kwargs['aws_access_key_id'] = getEnv(
                f'DY_{tablename}_TABLE_ACCESS_KEY_ID')
            kwargs['aws_secret_access_key'] = getEnv(
                f'DY_{tablename}_TABLE_SECRET_ACCESS_KEY')
            logger.info(f'use env table name : {env_tablename}')

        profile = getEnv('PROFILE', None)
        if profile is None:
            session = Session()
        else:
            session = Session(profile_name=profile)
        self.dynamodb = session.resource('dynamodb', **kwargs)
        self.table = self.dynamodb.Table(local_tablename)
        self.tablename = local_tablename

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def scan(self, **kwargs):
        return self.table.scan(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def query(self, **kwargs):
        return self.table.query(**kwargs)

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
        return self.table.update_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def put_item(self, **kwargs):
        return self.table.put_item(**kwargs)
    
    @retry(tries=2, delay=1, backoff=1, logger=logger)
    def get_item(self, **kwargs):
        return self.table.get_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def delete_item(self, **kwargs):
        return self.table.delete_item(**kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def batch_writer(self, **kwargs):
        """
        overwrite_by_pkeys=['partition_key', 'sort_key']
        """
        return self.table.batch_writer(**kwargs)

