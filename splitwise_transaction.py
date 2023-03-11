from transaction import Transaction
from dataclasses import dataclass


@dataclass
class SplitwiseTransaction(Transaction):
    personal_amount: float
