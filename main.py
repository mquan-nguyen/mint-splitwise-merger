import argparse
from rapidfuzz import process

def get_arguments():
    parser = argparse.ArgumentParser(
        prog='finance-reconciler',
        description='Reconcile finance spreadsheets')
    parser.add_argument('mint_filename', help='mint monthly transaction sheet')
    parser.add_argument('sw_filename', help='splitwise full transaction sheet')

    return parser.parse_args()

# something something tf-idf information retrieval class...... i'm kinda dumb for this and just want it to work
def find_similar_transaction(sw_description: str, mint_descriptions: list):
    return process.extract(sw_description, mint_descriptions)
    
# at some point, probably good to translate this out to OOP (make a transaction an obj)
# probably good to also add some margin of error (+-2 cents or something)
def find_same_price(sw_transaction: dict, mint_transactions: list):
    for x in mint_transactions:
        if sw_transaction["Total"] == x["Amount"]:
            return x
    
    return None

# matched -> {(splitwise, mint matching), ...}
# new transactions -> list of records
def find_matching_transactions(sw_transactions: list, mint_transactions: list):
    unmatched_transactions = []
    new_transactions = []
    matched_transactions = []
    for x in sw_transactions:# positive is me lending money, should have an existing transaction
        # negative is roselle lending money to me, does not have a transaction yet
        if (x["Personal Amount"] > 0): 
            matching_mint_transaction = find_same_price(x, mint_transactions)
            print(x["Description"], "->", matching_mint_transaction)

            if matching_mint_transaction:
                matched_transactions.append((x, find_same_price(x, mint_transactions)))
            else:
                unmatched_transactions.append(x)
        else:
            new_transactions.append(conform_transaction(x))
    return new_transactions, matched_transactions

# conform data structure to match mint's
def conform_transaction(sw_transaction):
    del sw_transaction["Total"]
    sw_transaction["Amount"] = abs(sw_transaction["Personal Amount"])
    del sw_transaction["Personal Amount"]
    sw_transaction["Category"] = ""

    return sw_transaction

# take matched transaction list & merge transaction amount to reflect net amount, not gross
# TODO: at some point should make the actual transaction list be a dict -> {hash involving date & description & amount: transaction}
# will make this a smiple implementation & faster, but oh well
def merge_matched(matched_list, mint_records):
    for splitwise, matching_mint in matched_list:
        index = mint_records.index(matching_mint)
        #consider maybe conforming matching splitwise amounts too? not sure
        print("Combining", splitwise["Description"], mint_records[index]["Date"] ,mint_records[index]["Amount"], "-", splitwise["Personal Amount"], "=", mint_records[index]["Amount"] - splitwise["Personal Amount"])
        mint_records[index]["Amount"] -= splitwise["Personal Amount"]

    return mint_records

def main():
    args = get_arguments()
    mint_records = parse_mint_transactions(args.mint_filename)
    sw_records = parse_splitwise_transactions(args.sw_filename, 1)
    new_transactions, matched_transactions = find_matching_transactions(sw_records, mint_records["records"])
    mint_records["records"] = merge_matched(matched_transactions, mint_records["records"])
    mint_records["records"].extend(new_transactions)
    
    df = pd.DataFrame.from_records(mint_records["records"])
    df.insert(3, "Inflow", '')
    df.insert(4, "Account", "Checking Account")
    df = df.sort_values(by=['Date'])
    print(df)
    print("Copying transactions to clipboard....")
    df.to_clipboard(index=False, header=False)
    


if __name__ == "__main__":
    main()