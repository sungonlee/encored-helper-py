from boto3.session import Session
import json
from retry import retry

from ejhelper2.helper.env import getEnv, AWS_PREFIX
from ejhelper2.helper.logging import getLogger

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

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def start_execution(self, **kawrgs):
        """
        Request Syntax
            response = client.start_execution(
                stateMachineArn='string',
                name='string',
                input='string',
                traceHeader='string'
            )
        Parameters
            stateMachineArn (string) --
                [REQUIRED]
                The Amazon Resource Name (ARN) of the state machine whose executions is listed.
            name (string) --
                The name of the execution. This name must be unique for your AWS account, region, and state machine for 90 days. For more information, see Limits Related to State Machine Executions in the AWS Step Functions Developer Guide .
                A name must not contain:
                    white space
                    brackets < > { } [ ]
                    wildcard characters ? *
                    special characters " # % \ ^ | ~ ` $ & , ; : /
                    control characters (U+0000-001F , U+007F-009F )
                    To enable logging with CloudWatch Logs, the name should only contain 0-9, A-Z, a-z, - and _.
            input (string) --
                The string that contains the JSON input data for the execution, for example:
                "input": "{\"first_name\" : \"test\"}"
            traceHeader (string) -- Passes the AWS X-Ray trace header. The trace header can also be passed in the request payload.


        Returns
            Response Syntax
            {
                'executionArn': 'string',
                'startDate': datetime(2015, 1, 1)
            }
        """
        logger.info(
            f'StepFunctions.start_execution kawrgs {json.dumps(kawrgs)}')
        return self.client.start_execution(**kawrgs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def stop_execution(self, **kawrgs):
        """
        Request Syntax
            response = client.stop_execution(
                executionArn='string',
                error='string',
                cause='string'
            )
        Parameters
            executionArn (string) --
                [REQUIRED]
                The Amazon Resource Name (ARN) of the execution to stop.
            error (string) -- The error code of the failure.
            cause (string) -- A more detailed explanation of the cause of the failure.

        Returns
            Response Syntax
            {
                'stopDate': datetime(2015, 1, 1)
            }
        """
        logger.info(
            f'StepFunctions.stop_execution kawrgs {json.dumps(kawrgs)}')
        return self.client.stop_execution(**kawrgs)
