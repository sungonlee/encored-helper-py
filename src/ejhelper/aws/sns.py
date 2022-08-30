from boto3.session import Session
from retry import retry

from ejhelper.helper.env import getEnv, AWS_PREFIX
from ejhelper.helper.logging import getLogger

logger = getLogger(__name__)

# 実行環境
env = getEnv(AWS_PREFIX)


class Sns:

    def __init__(self, **kwargs):
        profile = getEnv('PROFILE', None)
        if profile is None:
            session = Session()
        else:
            session = Session(profile_name=profile)
        self.sns = session.client('sns', **kwargs)

    @retry(tries=3, delay=1, backoff=1, logger=logger)
    def publish(self, **kwargs):
        """
        Request Syntax
            response = client.publish(
                TopicArn='string',
                TargetArn='string',
                                                PhoneNumber='string',
                                Message='string',
                                Subject='string',
                                MessageStructure='string',
                                MessageAttributes={
                                        'string': {
                                'DataType': 'string',
                                'StringValue': 'string',
                                'BinaryValue': b'bytes'
                                        }
                                },
                                MessageDeduplicationId='string',
                                MessageGroupId='string'
                                        )
                                        Parameters
                                TopicArn (string) --
                                The topic you want to publish to.

                                If you don't specify a value for the TopicArn parameter, you must specify a value for the PhoneNumber or TargetArn parameters.

                                TargetArn (string) -- If you don't specify a value for the TargetArn parameter, you must specify a value for the PhoneNumber or TopicArn parameters.
                                PhoneNumber (string) --
                                The phone number to which you want to deliver an SMS message. Use E.164 format.

                                If you don't specify a value for the PhoneNumber parameter, you must specify a value for the TargetArn or TopicArn parameters.

                                Message (string) --
                                [REQUIRED]

                                The message you want to send.

                                If you are publishing to a topic and you want to send the same message to all transport protocols, include the text of the message as a String value. If you want to send different messages for each transport protocol, set the value of the MessageStructure parameter to json and use a JSON object for the Message parameter.

                                Constraints:

                                With the exception of SMS, messages must be UTF-8 encoded strings and at most 256 KB in size (262,144 bytes, not 262,144 characters).
                                For SMS, each message can contain up to 140 characters. This character limit depends on the encoding schema. For example, an SMS message can contain 160 GSM characters, 140 ASCII characters, or 70 UCS-2 characters. If you publish a message that exceeds this size limit, Amazon SNS sends the message as multiple messages, each fitting within the size limit. Messages aren't truncated mid-word but are cut off at whole-word boundaries. The total size limit for a single SMS Publish action is 1,600 characters.
                                JSON-specific constraints:

                                Keys in the JSON object that correspond to supported transport protocols must have simple JSON string values.
                                The values will be parsed (unescaped) before they are used in outgoing messages.
                                Outbound notifications are JSON encoded (meaning that the characters will be reescaped for sending).
                                Values have a minimum length of 0 (the empty string, "", is allowed).
                                Values have a maximum length bounded by the overall message size (so, including multiple protocols may limit message sizes).
                                Non-string values will cause the key to be ignored.
                                Keys that do not correspond to supported transport protocols are ignored.
                                Duplicate keys are not allowed.
                                Failure to parse or validate any key or value in the message will cause the Publish call to return an error (no partial delivery).
                                Subject (string) --
                                Optional parameter to be used as the "Subject" line when the message is delivered to email endpoints. This field will also be included, if present, in the standard JSON messages delivered to other endpoints.

                                Constraints: Subjects must be ASCII text that begins with a letter, number, or punctuation mark; must not include line breaks or control characters; and must be less than 100 characters long.

                                MessageStructure (string) --
                                Set MessageStructure to json if you want to send a different message for each protocol. For example, using one publish action, you can send a short message to your SMS subscribers and a longer message to your email subscribers. If you set MessageStructure to json , the value of the Message parameter must:

                                be a syntactically valid JSON object; and
                                contain at least a top-level JSON key of "default" with a value that is a string.
                                You can define other top-level keys that define the message you want to send to a specific transport protocol (e.g., "http").

                                Valid value: json

                                MessageAttributes (dict) --
                                Message attributes for Publish action.

                                (string) --
                                (dict) --
                                The user-specified message attribute value. For string data types, the value attribute has the same restrictions on the content as the message body. For more information, see Publish .

                                Name, type, and value must not be empty or null. In addition, the message body should not be empty or null. All parts of the message attribute, including name, type, and value, are included in the message size restriction, which is currently 256 KB (262,144 bytes). For more information, see Amazon SNS message attributes and Publishing to a mobile phone in the Amazon SNS Developer Guide.

                                DataType (string) -- [REQUIRED]
                                Amazon SNS supports the following logical data types: String, String.Array, Number, and Binary. For more information, see Message Attribute Data Types .

                                StringValue (string) --
                                Strings are Unicode with UTF8 binary encoding. For a list of code values, see ASCII Printable Characters .

                                BinaryValue (bytes) --
                                Binary type attributes can store any binary data, for example, compressed data, encrypted data, or images.

                                MessageDeduplicationId (string) --
                                This parameter applies only to FIFO (first-in-first-out) topics. The MessageDeduplicationId can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9) and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~) .

                                Every message must have a unique MessageDeduplicationId , which is a token used for deduplication of sent messages. If a message with a particular MessageDeduplicationId is sent successfully, any message sent with the same MessageDeduplicationId during the 5-minute deduplication interval is treated as a duplicate.

                                If the topic has ContentBasedDeduplication set, the system generates a MessageDeduplicationId based on the contents of the message. Your MessageDeduplicationId overrides the generated one.

                                MessageGroupId (string) --
                                This parameter applies only to FIFO (first-in-first-out) topics. The MessageGroupId can contain up to 128 alphanumeric characters (a-z, A-Z, 0-9) and punctuation (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~) .

                                The MessageGroupId is a tag that specifies that a message belongs to a specific message group. Messages that belong to the same message group are processed in a FIFO manner (however, messages in different message groups might be processed out of order). Every message must include a MessageGroupId .

                                Return type
                                dict

                                Returns
                                Response Syntax
                                {
                                        'MessageId': 'string',
                                        'SequenceNumber': 'string'
                                }

                                Response Structure
                                (dict) --

                                Response for Publish action.

                                MessageId (string) --

                                Unique identifier assigned to the published message.
                                Length Constraint: Maximum 100 characters

                                SequenceNumber (string) --
                                This response element applies only to FIFO (first-in-first-out) topics.
                                The sequence number is a large, non-consecutive number that Amazon SNS assigns to each message. The length of SequenceNumber is 128 bits. SequenceNumber continues to increase for each MessageGroupId .

                                Exceptions
                                SNS.Client.exceptions.InvalidParameterException
                                SNS.Client.exceptions.InvalidParameterValueException
                                SNS.Client.exceptions.InternalErrorException
                                SNS.Client.exceptions.NotFoundException
                                SNS.Client.exceptions.EndpointDisabledException
                                SNS.Client.exceptions.PlatformApplicationDisabledException
                                SNS.Client.exceptions.AuthorizationErrorException
                                SNS.Client.exceptions.KMSDisabledException
                                SNS.Client.exceptions.KMSInvalidStateException
                                SNS.Client.exceptions.KMSNotFoundException
                                SNS.Client.exceptions.KMSOptInRequired
                                SNS.Client.exceptions.KMSThrottlingException
                                SNS.Client.exceptions.KMSAccessDeniedException
                                SNS.Client.exceptions.InvalidSecurityException
                """
        self.sns.publish(**kwargs)
