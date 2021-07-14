import boto3
from retry import retry

from ejhelper.helper.logging import getLogger

logger = getLogger(__name__)


class DynamoDBTable:

    def __init__(self, table_name, **kwargs):

        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb', **kwargs)
        self.table = self.dynamodb.Table(self.table_name)

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
