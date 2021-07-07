import math
import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return o


def decimalEncoder(o):
    if isinstance(o, decimal.Decimal):
        if o % 1 > 0:
            return float(o)
        else:
            return int(o)
    return o


def normalRound(val, digit=0):
    """
    roundは通常の四拾五入にならないため、
    参考：https://note.nkmk.me/python-round-decimal-quantize/
    """
    local_val = decimalEncoder(val)
    p = 10 ** digit
    s = math.copysign(1, local_val)
    return (s * local_val * p * 2 + 1) // 2 / p * s
