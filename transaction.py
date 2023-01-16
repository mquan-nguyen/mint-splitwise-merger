from dataclasses import dataclass
from datetime import date

# End result transaction. Most resembles the Mint transactions, and what is put into the excel sheet at the end
@dataclass
class Transaction:
    date: date
    category: str
    description: str
    amount: float

    def to_hash() -> str:
        pass #CRC32 hash?