from django.contrib.auth.models import User
from transactions.models import Transaction
from django.utils import timezone
import csv
from datetime import datetime
from decimal import Decimal

def map_privat_category(category):
    """Maps PrivatBank categories to our model categories"""
    category_mapping = {
        'Розваги': 'entertainment',
        'Цифрові товари': 'digital_goods',
        'Їжа та напої': 'food_drink',
    }
    return category_mapping.get(category, 'other')

def import_privat_bank_csv(file_path):
    """
    Import transactions from PrivatBank CSV file.
    
    Args:
        file_path (str): Path to the CSV file
    
    Returns:
        tuple: (success_count, error_count, error_messages)
    """
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        raise ValueError("No superuser found in the database!")

    success_count = 0
    error_count = 0
    error_messages = []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            # Skip the first line as it contains the date range
            next(file)
            
            reader = csv.DictReader(file)
            
            for row_number, row in enumerate(reader, start=2):  # Start from 2 to account for header
                try:
                    # Parse and validate date
                    date = datetime.strptime(row["Дата"], "%d.%m.%Y %H:%M:%S")
                    
                    # Parse amount and determine transaction type
                    amount = Decimal(row["Сума в валюті картки"].replace(',', '.'))
                    if amount < 0:
                        type = 'expense'
                        amount = abs(amount)
                    else:
                        type = 'income'

                    # Parse original amount
                    original_amount = Decimal(row["Сума в валюті транзакції"].replace(',', '.'))
                    if type == 'expense':
                        original_amount = abs(original_amount)
                    
                    # Parse balance
                    balance = Decimal(row["Залишок на кінець періоду"].replace(',', '.'))
                    
                    # Map category
                    category = map_privat_category(row["Категорія"])
                    
                    # Create transaction
                    Transaction.objects.create(
                        user=superuser,
                        date=date,
                        category=category,
                        card=row["Картка"],
                        vendor=row["Опис операції"].strip('*'),  # Remove asterisks
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

# didn't look at properly
def import_oschad_bank_csv(file_path):
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        print("No superuser found!")
        return

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                date = datetime.datetime.strptime(row["date"], "%d %B %Y %H:%M")
                category = 'other'
                description = row["decription"]
                income = row["income"].replace(",", ".")  # Handle decimal separator
                debits = row["debits"].replace(",", ".")
                balance = row["balance"].replace(",", ".")

                amount = float(income) if income else -float(debits)
                currency = "UAH"  # Assuming UAH since no currency column exists

                Transaction.objects.create(
                    user=superuser,
                    date=date,
                    category=category,
                    description=description,
                    amount=amount,
                    currency=currency,
                    balance_after_transaction=float(balance),
                    transaction_source="OschadBank",
                )

            except Exception as e:
                print(f"Skipping row due to error: {e}")

    print("OschadBank CSV Import Complete!")

