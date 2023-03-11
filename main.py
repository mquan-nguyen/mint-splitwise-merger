import argparse
from csv_parser import *

def get_arguments():
    parser = argparse.ArgumentParser(
        prog='finance-reconciler',
        description='Reconcile finance spreadsheets')
    parser.add_argument('mint_filename', help='mint monthly transaction sheet')
    parser.add_argument('sw_filename', help='splitwise full transaction sheet')

    return parser.parse_args()

def main():
    args = get_arguments()
    mint_ledger = parse_mint_transactions(args.mint_filename)
    sw_ledger = parse_splitwise_transactions(args.sw_filename, 2)

    mint_ledger.merge_ledger(sw_ledger)
    
    mint_ledger.to_clipboard()
    
    


if __name__ == "__main__":
    main()