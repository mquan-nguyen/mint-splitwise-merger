from dataclasses import dataclass
from datetime import date
import zlib

# interface for transactions
@dataclass
class Transaction:
    date: date
    description: str

    def to_hash(self) -> int:
        pass

# interface for transactions
@dataclass
class MintTransaction(Transaction):
    category: str
    amount: float

    def to_hash(self) -> int:
        transaction_string = str(self.date) + self.description + str(self.amount)
        return zlib.adler32(bytes(transaction_string, "ascii"))

@dataclass
class SplitwiseTransaction(Transaction):
    total_amount: float
    personal_amount: float

    def to_hash(self) -> int:
        # add total amt since that is what we are matching on for Mint Transactions
        transaction_string = str(self.date) + self.description + str(self.total_amount)
        return zlib.adler32(bytes(transaction_string, "ascii"))
