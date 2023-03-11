from transaction import Transaction
from dataclasses import dataclass


@dataclass
class MintTransaction(Transaction):
    personal_amount: float
