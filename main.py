#!/usr/bin/env python
import argparse
import os
import sys

import file_impex

EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'exports'))


def main() -> None:
    args = parse_args()
    loan_transactions: list = file_impex.load_loan_transactions_from_csv(filename=args.file, folder=args.destination)
    print_summary(loan_transactions=loan_transactions)
    file_impex.save_loan_transactions_to_csv(loan_transactions=loan_transactions, folder=args.destination)


def print_summary(loan_transactions: list) -> None:
    interests: list = [transaction['value'] for transaction in loan_transactions if transaction]

    if len(interests) <= 0:
        return
    avg_interest: float = sum(interests) / float(len(interests))

    sys.stdout.write('===== SUMMARY =====\r\n')
    sys.stdout.write(f'{len(interests)} transactions of interests: SUM={sum(interests)} AVG={avg_interest} MIN={min(interests)} MAX={max(interests)}\r\n')
    sys.stdout.write('===================\r\n\r\n')
    sys.stdout.flush()


def parse_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-f", "--file", help="input CSV file - exported from Trine", required=True)
    argparser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", required=False)
    argparser.add_argument("-d", "--destination", help="destination folder for result CSV file", required=False,
                           default=EXPORTS_FOLDER)
    args = argparser.parse_args()
    return args


if __name__ == "__main__":
    main()
