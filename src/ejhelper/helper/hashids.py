from hashids import Hashids


class HashIds():

    def __init__(self) -> None:

        self.hashids = Hashids('EnertalkConnectPrj', 8,
                               '0123456789abcdefghijklmnopqrstuvwxyz')

    def encode(self, args: str) -> str:
        return self.hashids.encode(args)

    def decode(self, args: str) -> int:
        return sum(self.hashids.decode(args))
