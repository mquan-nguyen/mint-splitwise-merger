from transaction import Transaction
from dataclasses import dataclass, field
from typing import Dict

# Holds all the transactions

@dataclass
class Ledger:
    # hash -> transaction
    records: Dict[int, Transaction] = field(default_factory=dict)

    def add_transaction(self, t):
        # raise exception if fields are no good... yare yare
        self.records[t.to_hash()] = t
    
    def remove_transaction(self, t):
        del self.records[t.to_hash()]

    def merge_ledger(self, other):
        pass

    def to_clipboard():
        pass