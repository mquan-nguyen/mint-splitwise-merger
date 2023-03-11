import pandas as pd
from ledger import Ledger
from transaction import *

MINT_CAT_FILTERS = [
    "Credit Card Payment",
    "Hide from Budgets & Trends",
    ]

def dataframe_to_mint_ledger(df):
    book = Ledger()
    for x in df.iterrows():
        x = x[1]
        book.add_transaction(MintTransaction
                             (
                              date=x["Date"], 
                              category=x["Category"],
                              description=x["Description"], 
                              amount=x["Amount"]
                              )
                            )
    return book


# there's definitely a cleaner way to do this
def dataframe_to_splitwise_ledger(df):
    book = Ledger()
    for x in df.iterrows():
        x = x[1]
        # TBD -> splitwise.amount = total & splitwise.personal_amount = personal amount?
        book.add_transaction(
            SplitwiseTransaction(
                date=x["Date"], 
                description=x["Description"], 
                total_amount=x["Total"], 
                personal_amount=x["Personal Amount"]
            )
        )
    return book

# "Date","Description","Original Description","Amount","Transaction Type","Category","Account Name","Labels","Notes"
def parse_mint_transactions(filename: str):
    mint = pd.read_csv(filename, parse_dates=["Date"])
    mint = mint[~mint["Category"].isin(MINT_CAT_FILTERS)]
    mint = mint[["Date", "Description", "Amount", "Category"]]
    mint = mint.sort_values(by=['Date'])
    print("------------------")
    print("Mint Transactions")
    print("------------------")
    print(mint)
    return dataframe_to_mint_ledger(mint)

# Date,Description,Category,Cost,Currency,Matthew Nguyen,Roselle Ardosa
def parse_splitwise_transactions(filename: str, month: int):
    sw = pd.read_csv(filename, parse_dates=["Date"])
    sw = sw[sw["Date"].dt.month == month]
    sw = sw[sw["Description"] != "Total balance"]
    sw = sw[~(sw["Description"].str.contains("Roselle A. paid Matthew N.") | sw["Description"].str.contains("Matthew N. paid Roselle A."))]
    sw = sw[["Date", "Description", "Cost", "Matthew Nguyen"]]
    sw = sw.rename({"Cost": "Total", "Matthew Nguyen": "Personal Amount"}, axis='columns')
    # not sure why it converts Total to a string, but it does
    sw["Total"] = sw["Total"].astype(float)
    sw = sw.sort_values(by=['Date'])
    print("-----------------------")
    print("Splitwise Transactions")
    print("-----------------------")
    print(sw)
    return dataframe_to_splitwise_ledger(sw)