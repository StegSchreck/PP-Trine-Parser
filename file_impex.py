import csv
import datetime
import os
import sys
import time
from typing import Optional

TIMESTAMP: str = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
CSV_HEADER: str = 'Datum,Wert,Buchungswährung,Typ,Notiz\n'
REPAID_INTEREST = "RepaidInterest"
LATE_FEE = "LateFee"
DATE = "Date"


def load_loan_transactions_from_csv(folder: str, filename: str) -> list:
    sys.stdout.write('===== loading loan transactions from CSV\r\n')
    sys.stdout.write(f'      folder: {folder}\r\n')
    sys.stdout.write(f'      filename: {filename}\r\n')
    sys.stdout.write('\r\n')
    sys.stdout.flush()
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'r', newline="", encoding='UTF-8') as input_file:
        reader = csv.reader(input_file, delimiter=",")
        headers = next(reader, None)
        return [convert_csv_row_to_transaction(headers, row) for row in reader]


def convert_csv_row_to_transaction(headers, row) -> Optional[dict]:
    if not row[headers.index(DATE)]:
        # ignore lines with no date (reserved investments)
        return None
    transaction = dict()
    if "/" in row[headers.index(DATE)]:
        transaction_date = datetime.datetime.strptime(row[headers.index(DATE)], '%m/%d/%Y')
    else:
        transaction_date = datetime.datetime.strptime(row[headers.index(DATE)], '%Y-%m-%d')
    transaction['date'] = transaction_date.strftime('%Y-%m-%d')
    interest: float = float(row[headers.index(REPAID_INTEREST)]) if REPAID_INTEREST in headers and row[headers.index(REPAID_INTEREST)] else 0.0
    late_fees = float(row[headers.index(LATE_FEE)]) if LATE_FEE in headers and row[headers.index(LATE_FEE)] else 0.0
    transaction['value'] = interest + late_fees
    transaction['type'] = 'Zinsen'
    transaction['id'] = f'{row[headers.index("Type")]} - {row[headers.index("Loan")]}'
    if transaction['value'] > 0:
        return transaction
    return None


def save_loan_transactions_to_csv(loan_transactions: list, folder: str, filename: str = f'{TIMESTAMP}_trine.csv') -> None:
    sys.stdout.write('===== saving loan transactions to CSV\r\n')
    sys.stdout.write(f'      folder: {folder}\r\n')
    sys.stdout.write(f'      filename: {filename}\r\n')
    sys.stdout.write(f'      number of entries: {len(loan_transactions)}\r\n')
    sys.stdout.flush()
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'w+', encoding='UTF-8') as output_file:
        output_file.write(CSV_HEADER)
        for transaction in loan_transactions:
            if transaction:
                output_file.write(convert_transaction_to_csv_row(transaction))


def convert_transaction_to_csv_row(transaction: dict) -> str:
    transaction_csv_row: str = f"{transaction['date']}," \
                               f"\"{str(transaction['value']).replace('.', ',')}\"," \
                               "EUR," \
                               f"{transaction['type']}," \
                               f"{transaction['id']}," \
                               f"\n"
    return transaction_csv_row
