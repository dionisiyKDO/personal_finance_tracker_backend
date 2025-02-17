from django.contrib.auth.models import User
from transactions.models import Transaction
from django.utils import timezone
import csv
from datetime import datetime
from decimal import Decimal

def import_privat_bank_csv(file_path):
    """Import transactions from PrivatBank CSV file."""
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        raise ValueError("No superuser found in the database!")

    success_count = 0
    error_count = 0
    error_messages = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            next(file) # Skip the first line as it contains the date range

            reader = csv.DictReader(file)

            for row_number, row in enumerate(
                reader, start=2
            ):  # Start from 2 to account for header
                try:
                    # Parse and validate date
                    date = datetime.strptime(row["Дата"], "%d.%m.%Y %H:%M:%S")

                    # Parse amount and determine transaction type
                    amount = Decimal(row["Сума в валюті картки"].replace(",", "."))
                    if amount < 0:
                        type = "expense"
                        amount = abs(amount)
                    else:
                        type = "income"

                    # Parse original amount
                    original_amount = Decimal(
                        row["Сума в валюті транзакції"].replace(",", ".")
                    )
                    if type == "expense":
                        original_amount = abs(original_amount)

                    # Parse balance
                    balance = Decimal(
                        row["Залишок на кінець періоду"].replace(",", ".")
                    )
                    
                    # Get vendor
                    vendor = row["Опис операції"].strip("*")
                    
                    # Create transaction
                    Transaction.objects.create(
                        user=superuser,
                        date=date,
                        card=row["Картка"],
                        vendor=vendor,
                        type=type,
                        amount=amount,
                        currency=row["Валюта картки"],
                        original_amount=original_amount,
                        original_currency=row["Валюта транзакції"],
                        balance_after_transaction=balance,
                        transaction_source="PrivatBank",
                    )
                    success_count += 1

                except KeyError as e:
                    error_msg = f"Row {row_number}: Missing required column: {str(e)}"
                    error_messages.append(error_msg)
                    error_count += 1
                except ValueError as e:
                    error_msg = f"Row {row_number}: Invalid value: {str(e)}"
                    error_messages.append(error_msg)
                except Exception as e:
                    error_msg = f"Row {row_number}: Unexpected error: {str(e)}"
                    error_messages.append(error_msg)
                    error_count += 1

    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {str(e)}")

    # Print summary
    print("\nImport Summary:")
    print(f"Successfully imported: {success_count} transactions")
    if error_count:
        print(f"Errors encountered: {error_count}")
        print("\nError Details:")
        for msg in error_messages:
            print(f"- {msg}")

    return success_count, error_count, error_messages


def import_oschad_csv(file_path: str):
    """Import transactions from an Oschad CSV file."""
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        raise ValueError("No superuser found in the database!")

    def parse_oschad_date(date_str: str) -> datetime:
        """
        Parse a Ukrainian date string from an Oschad CSV.

        Expected formats:
            "3 лютого 2025 00:00" or "3 лютого 2025"
        """
        parts = date_str.strip().split()
        if len(parts) < 3:
            raise ValueError(f"Date string '{date_str}' has insufficient parts")

        day = parts[0]
        month_name = parts[1].lower()
        year = parts[2]
        month_map = {
            "січня": "01",
            "лютого": "02",
            "березня": "03",
            "квітня": "04",
            "травня": "05",
            "червня": "06",
            "липня": "07",
            "серпня": "08",
            "вересня": "09",
            "жовтня": "10",
            "листопада": "11",
            "грудня": "12",
        }
        month = month_map.get(month_name)
        if not month:
            raise ValueError(f"Unknown month name: {month_name}")

        if len(parts) >= 4:
            time_part = parts[3]
            # Ensure day is two digits
            date_formatted = f"{day.zfill(2)}/{month}/{year} {time_part}"
            fmt = "%d/%m/%Y %H:%M"
        else:
            date_formatted = f"{day.zfill(2)}/{month}/{year}"
            fmt = "%d/%m/%Y"

        return datetime.strptime(date_formatted, fmt)

    success_count = 0
    error_count = 0
    error_messages = []

    try:
        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
            # Use DictReader to handle headers and possible extra empty columns.
            reader = csv.DictReader(file)

            # Normalize header keys by stripping whitespace.
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames if name]

            for row_number, row in enumerate(reader, start=2):
                try:
                    # Ensure required fields exist (e.g., date and description).
                    # Good but description can blank, and date can't be blank, so the point is not valid
                    # if not row.get("date") or not row.get("description"):
                    #     raise ValueError("Missing required fields in row")

                    # Parse date using the custom parser.
                    date = parse_oschad_date(row["date"])

                    # Determine vendor and description.
                    # Use "who" for vendor; if not available, fallback to "on_what".
                    vendor_raw = row.get("who") or row.get("on_what") or ""
                    vendor = vendor_raw.strip("*").strip()

                    # Handle the typo in the header: use "decription" if "description" is absent.
                    description = (
                        row.get("description") or row.get("decription") or ""
                    ).strip()

                    # Get income and debits values.
                    income_str = row.get("income", "").strip()
                    debits_str = row.get("debits", "").strip()

                    # Determine transaction type and amount.
                    if income_str and income_str not in ["*", ""]:
                        transaction_type = "income"
                        amount = Decimal(income_str.replace(",", "."))
                    elif debits_str and debits_str not in ["*", ""]:
                        transaction_type = "expense"
                        amount = Decimal(debits_str.replace(",", "."))
                    else:
                        raise ValueError("No valid amount found in row")

                    # Parse balance, if provided.
                    balance_raw = row.get("balance", "").strip()
                    balance_after_transaction = (
                        Decimal(balance_raw.replace(",", ".")) if balance_raw else None
                    )

                    Transaction.objects.create(
                        user=superuser,
                        date=date,
                        card="5167 **** **** 8163",
                        type=transaction_type,
                        amount=amount,
                        currency="UAH",
                        description=description,
                        vendor=vendor,
                        balance_after_transaction=balance_after_transaction,
                        transaction_source="OschadBank",
                    )
                    success_count += 1
                except KeyError as e:
                    error_messages.append(
                        f"Row {row_number}: Missing required column: {str(e)}"
                    )
                    error_count += 1
                except Exception as e:
                    error_messages.append(f"Row {row_number}: Error: {str(e)}")
                    error_count += 1
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading CSV file: {str(e)}")

    print("\nImport Summary (Oschad):")
    print(f"Successfully imported: {success_count} transactions")
    if error_count:
        print(f"Errors encountered: {error_count}")
        for msg in error_messages:
            print(f"- {msg}")

    return success_count, error_count, error_messages
