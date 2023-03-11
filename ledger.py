from transaction import Transaction
from dataclasses import dataclass, field, asdict
from typing import Dict
import pandas as pd

# Holds all the transactions

@dataclass
class Ledger:
    # hash -> transaction
    records: Dict[str, Transaction] = field(default_factory=dict)

    def add_splitwise_transactions(self, to_add):
        for x in to_add:
            self.add_transaction(x.convert_to_mint_transaction())
    
    def add_transaction(self, t):
        # raise exception if fields are no good... yare yare
        self.records[t.to_hash()] = t
    
    def remove_transaction(self, t):
        del self.records[t.to_hash()]

    def merge_ledger(self, other): #Other being Ledger w/ Splitwise transactions
        # find matching transactions
        # merge splitwise & mint transactions, add transactions that did not exist
        to_merge, to_add = self._find_matching_transactions(other)
        self._merge_transactions(to_merge)
        self.add_splitwise_transactions(to_add)

    def _find_matching_transactions(self, other):
        # probably would be good to have Ledger be iterable, but lazy to write        

        new_transactions = []
        to_merge_transactions = []
        for t in other.records.values():
            # transactions w/ negative personal amount means i owe that much
            # positive personal amt means I paid this much for them, so total cost - personal amt = my true amt           
            if t.personal_amount > 0:
                to_merge_transactions.append(t)
            else:
                new_transactions.append(t)

        matched_transactions = self._match_based_on_amount(to_merge_transactions)

        return matched_transactions, new_transactions

        
    def _match_based_on_amount(self, splitwise_to_match_on):
        matched_transactions = {}
        for sw in splitwise_to_match_on:
            # it's not likely that there are multiple mint transactions that match a splitwise transactions, but is an edge case
            # it would be nice to have the amt be the key, but it's not a unique key :l
            for hash, m_transaction in self.records.items():
                if sw.total_amount == m_transaction.amount:
                    matched_transactions[hash] = sw
                    break
        if len(splitwise_to_match_on) != len(matched_transactions):
            print("There are some unmatched transactions leftover!")
            print("not matched", [x for x in splitwise_to_match_on if x not in matched_transactions.values()])
        return matched_transactions
    
    # expects dict of matching mint hash -> splitwise transaction
    def _merge_transactions(self, matched_transactions):
        for hash, sw_transaction in matched_transactions.items():
            # total amt reflected in mint, personal_amt is how much i "lent" to roselle
            self.records[hash].amount -= sw_transaction.personal_amount


    def to_clipboard(self):
        # Add additional columns to match spreadsheet
        df = pd.DataFrame.from_records([asdict(x) for x in self.records.values()])
        df.insert(3, "Inflow", '')
        df.insert(4, "Account", "Checking Account")
        df = df.sort_values(by=['date'])
        print("Copying transactions to clipboard....")
        print(df)
        df.to_clipboard(index=False, header=False)