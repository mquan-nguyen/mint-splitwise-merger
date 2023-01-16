from transaction import Transaction
from dataclasses import dataclass, List

# Holds all the transactions

@dataclass
class Ledger:
    records: list[Transaction]

    def append_transaction(self, t):
        # raise exception if fields are no good... yare yare
        self.records.append(t)

    def to_clipboard():
        pass