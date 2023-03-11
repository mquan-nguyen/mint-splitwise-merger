from dataclasses import dataclass
from datetime import date
import zlib

# End result transaction. Most resembles the Mint transactions, and what is put into the excel sheet at the end
@dataclass
class Transaction:
    # TODO NEXT: BRANCH OFF INTO MINT TRANSACTION & SPLITWISE TRANSACTION, MINT HAS CATEGORY SPLITWISE HAS PERSONAL AMT 
    date: date
    category: str
    description: str
    amount: float

    def to_hash(self) -> str:
        transaction_string = str(self.date) + self.description + str(self.amount)
        return zlib.adler32(bytes(transaction_string, "ascii"))