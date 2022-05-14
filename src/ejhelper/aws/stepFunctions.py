from boto3.session import Session
import json
from retry import retry

from ejhelper.helper.env import getEnv, AWS_PREFIX
from ejhelper.helper.logging import getLogger

logger = getLogger(__name__)

# 実行環境
env = getEnv(AWS_PREFIX)


class StepFunctions:

    def __init__(self, **kwargs):

        profile = getEnv('PROFILE', None)
        if profile is None:
            session = Session()
        else:
            session = Session(profile_name=profile)
        self.client = session.client('stepfunctions', **kwargs)

    @staticmethod
    def maka_arn_by_name(stateMachineName, region, accountId) -> str:
        return getEnv(f'SFN_{stateMachineName}', f'arn:aws:states:${region}:${accountId}:stateMachine:${stateMachineName}')

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def list_executions(self, **kwargs):
        """
        Request Syntax
            response = client.list_executions(
                stateMachineArn='string',
                statusFilter='RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED',
                maxResults=123,
                nextToken='string'
            )
        Parameters
            stateMachineArn (string) --
                [REQUIRED]
                The Amazon Resource Name (ARN) of the state machine whose executions is listed.
            statusFilter (string) -- If specified, only list the executions whose current execution status matches the given filter.
            maxResults (integer) --
                The maximum number of results that are returned per call. You can use nextToken to obtain further pages of results. The default is 100 and the maximum allowed page size is 1000. A value of 0 uses the default.
                This is only an upper limit. The actual number of results returned per call might be fewer than the specified maximum.
            nextToken (string) -- If nextToken is returned, there are more results available. The value of nextToken is a unique pagination token for each page. Make the call again using the returned token to retrieve the next page. Keep all other arguments unchanged. Each pagination token expires after 24 hours. Using an expired pagination token will return an HTTP 400 InvalidToken error.
        Returns
            Response Syntax
            {
                'executions': [
                    {
                        'executionArn': 'string',
                        'stateMachineArn': 'string',
                        'name': 'string',
                        'status': 'RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED',
                        'startDate': datetime(2015, 1, 1),
                        'stopDate': datetime(2015, 1, 1)
                    },
                ],
                'nextToken': 'string'
            }
        """
        logger.info(
            f'StepFunctions.list_executions kwargs {json.dumps(kwargs)}')
        return self.client.list_executions(**kwargs)
