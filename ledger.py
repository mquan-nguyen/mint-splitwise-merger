from transaction import Transaction
from dataclasses import dataclass, Dict

# Holds all the transactions

@dataclass
class Ledger:
    # hash -> transaction
    records: Dict[int, Transaction]

    def append_transaction(self, t):
        # raise exception if fields are no good... yare yare
        self.records.append(t)
    
    def remove_transaction(self, t):
        pass

    def merge_ledger(self, other):
        pass

    def to_clipboard():
        pass