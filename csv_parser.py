import pandas as pd

MINT_CAT_FILTERS = [
    "Credit Card Payment",
    "Hide from Budgets & Trends",
    ]

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
    return {"all_descriptions": mint["Description"].to_list(), "records": mint.to_dict("records")}

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
    return sw.to_dict("records")