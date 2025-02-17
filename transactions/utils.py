from django.contrib.auth.models import User
from django.utils import timezone

from transactions.models import Transaction

from datetime import datetime
from decimal import Decimal
import csv

import warnings
import logging
import colorlog


def init_logger():
    """Initializes the logger with a custom format."""
    log_format = "%(log_color)s%(levelname)s%(reset)s: %(asctime)s.%(msecs)03d - %(message)s%(reset)s"
    color_formatter = colorlog.ColoredFormatter(
        log_format,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])


warnings.simplefilter(action="ignore", category=RuntimeWarning)
logger = logging.getLogger(__name__)
init_logger()


def import_privat_bank_csv(file_path):
    """Import transactions from PrivatBank CSV file."""
    logger.info(f"Starting import of PrivatBank CSV: {file_path}")

    # TODO: Implement different users, not just superuser
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        logger.error("No superuser found in the database!")
        raise ValueError("No superuser found in the database!")

    success_count = 0
    error_count = 0
    error_messages = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            next(file)  # Skip the first line as it contains the date range
            reader = csv.DictReader(file)

            for row_number, row in enumerate(
                reader, start=2
            ):  # Start from 2 to account for header
                try:
                    # Parse and validate date
                    date = datetime.strptime(row["Дата"], "%d.%m.%Y %H:%M:%S")

                    # Parse amount and determine transaction type
                    amount = Decimal(row["Сума в валюті картки"].replace(",", "."))
                    type = "income" if amount > 0 else "expense"
                    amount = abs(amount)

                    # Parse original amount, and balance
                    original_amount = Decimal(
                        row["Сума в валюті транзакції"].replace(",", ".")
                    )
                    balance = Decimal(
                        row["Залишок на кінець періоду"].replace(",", ".")
                    )

                    # Create transaction
                    Transaction.objects.create(
                        user=user,
                        date=date,
                        card=row["Картка"],
                        vendor=row["Опис операції"].strip("*"),
                        type=type,
                        amount=amount,
                        currency=row["Валюта картки"],
                        original_amount=original_amount,
                        original_currency=row["Валюта транзакції"],
                        balance_after_transaction=balance,
                        transaction_source="PrivatBank",
                    )
                    success_count += 1
                    logger.info(f"Row {row_number}: Transaction imported successfully.")

                except Exception as e:
                    error_msg = f"Row {row_number}: {str(e)}"
                    error_messages.append(error_msg)
                    error_count += 1
                    logger.error(error_msg)

    except FileNotFoundError:
        logger.critical(f"CSV file not found: {file_path}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error reading CSV file: {str(e)}")
        raise

    # Print summary
    logger.info(
        f"PrivatBank Import Summary: {success_count} successes, {error_count} errors."
    )
    return success_count, error_count, error_messages


def import_oschad_csv(file_path: str):
    """Import transactions from my manually written Oschad CSV file."""
    logger.info(f"Starting import of Oschad CSV: {file_path}")

    user = User.objects.filter(is_superuser=True).first()
    if not user:
        logger.error("No superuser found in the database!")
        raise ValueError("No superuser found in the database!")

    success_count = 0
    error_count = 0
    error_messages = []

    def parse_oschad_date(date_str: str) -> datetime:
        """
        Parse a Ukrainian date string from an Oschad CSV.

        Expected formats:
            "3 лютого 2025 00:00" or "3 лютого 2025"
        """
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

        parts = date_str.strip().split()
        if len(parts) < 3:
            raise ValueError(f"Date string '{date_str}' has insufficient parts")

        day = parts[0]
        month_name = parts[1]
        year = parts[2]

        month = month_map.get(month_name.lower())
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

    try:
        with open(file_path, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            # Normalize header keys by stripping whitespace.
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames if name]

            for row_number, row in enumerate(reader, start=2):
                try:
                    # Parse date
                    date = parse_oschad_date(row["date"])

                    # Determine vendor and description. Use "who" for vendor; if not available, fallback to "on_what".
                    vendor_raw = row.get("who") or row.get("on_what") or ""
                    vendor = vendor_raw.strip("*").strip()
                    description = row.get("description").strip()

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
                    balance = Decimal(row.get("balance", "0").replace(",", "."))

                    Transaction.objects.create(
                        user=user,
                        date=date,
                        card="5167 **** **** 8163",
                        type=transaction_type,
                        amount=amount,
                        currency="UAH",
                        description=description,
                        vendor=vendor,
                        balance_after_transaction=balance,
                        transaction_source="OschadBank",
                    )
                    success_count += 1
                    logger.info(f"Row {row_number}: Transaction imported successfully.")

                except Exception as e:
                    error_msg = f"Row {row_number}: {str(e)}"
                    error_messages.append(error_msg)
                    error_count += 1
                    logger.error(error_msg)
    except FileNotFoundError:
        logger.critical(f"CSV file not found: {file_path}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error reading CSV file: {str(e)}")
        raise

    logger.info(f"OschadBank Import Summary: {success_count} successes, {error_count} errors.")
    return success_count, error_count, error_messages
