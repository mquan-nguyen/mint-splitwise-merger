import argparse
from csv_parser import *
import pyinputplus as pyip
from datetime import date


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='finance-reconciler',
        description='Reconcile finance spreadsheets')
    parser.add_argument('mint_filename', help='mint monthly transaction sheet')
    parser.add_argument('sw_filename', help='splitwise full transaction sheet')

    return parser.parse_args()

def ask_date_input():
    date_input = pyip.inputDate("YYYY-MM-DD after to consider Splitwise transactions (Enter to default to this month): ", blank=True, formats=["%Y-%m-%d"])
    if date_input == "":
        date_input = date(date.today().year, date.today().month, 1)
    return str(date_input)

def main():
    args = get_arguments()
    mint_ledger = parse_mint_transactions(args.mint_filename)
    date_str = ask_date_input()
    sw_ledger = parse_splitwise_transactions(args.sw_filename, date_str)

    mint_ledger.merge_ledger(sw_ledger)
    
    mint_ledger.to_clipboard()
    
    


if __name__ == "__main__":
    main()