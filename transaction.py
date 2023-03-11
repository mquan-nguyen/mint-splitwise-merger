from dataclasses import dataclass
from datetime import date
import zlib

# interface for transactions
@dataclass
class Transaction:
    date: date
    description: str

    def to_hash(self) -> str:
        pass

# interface for transactions
@dataclass
class MintTransaction(Transaction):
    category: str
    amount: float

    def to_hash(self) -> str:
        transaction_string = str(self.date) + self.description + str(self.amount)
        return zlib.adler32(bytes(transaction_string, "utf-8"))

@dataclass
class SplitwiseTransaction(Transaction):
    total_amount: float
    personal_amount: float

    def convert_to_mint_transaction(self) -> MintTransaction:
        return MintTransaction(
            date = self.date, 
            description = self.description,
            category = "",
            amount = abs(self.personal_amount) #negative personal amounts = new transactions
        )
    
    def to_hash(self) -> str:
        # add total amt since that is what we are matching on for Mint Transactions
        transaction_string = str(self.date) + self.description + str(self.total_amount)
        return zlib.adler32(bytes(transaction_string, "utf-8"))
