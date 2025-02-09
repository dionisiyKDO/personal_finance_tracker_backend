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

def map_vendor_name(vendor_name):
    """
    Maps a vendor name from a receipt to a more readable and understandable name.
    
    Args:
        vendor_name (str): The vendor name as it appears on the receipt.
    
    Returns:
        str: The mapped, readable vendor name.
    """
    vendor_mapping = {
        "Мобильный": "Mobile Service Provider",
        "MONODirect KYIV UKR": "MONO Bank (Ukraine)",
        "На другую карту": "Transfer to Another Card",
        "С другой карты": "From Another Card",
        "Стипендия": "NU Zaporizhzhia Polytechnic: Scholarship",
        "Нова пошта": "Nova Poshta (Courier Service)",
        "UDEMY ONLINE COURSES": "Udemy",
        "Терминал": "Terminal (ATM/POS)",
        "GOOGLE *Duolingo": "Google play (Duolingo)",
        "RozetkaPay": "Rozetka (Online Store)",
        "RAHIMI31": "unknown",
        "IBOX BANK A2C": "Terminal (ATM/POS)",
        "IBOX CASH TO CARD": "Terminal (ATM/POS)",
        "Amazon Video*2P28C8DW4": "Amazon Prime Video",
        "MooGold Enterprise": "MooGold (Gaming/Online Service)",
        "GLOBAL24": "unknown",
        
        "Сільпо": "Zaporizhzhia Store (Ukraine)",
        "Kompyuteritakomplektuy": "Zaporizhzhia Store (Ukraine)",
        "L10A ZAPOROZHYE UKR": "Zaporizhzhia Store (Ukraine)",
        "ZAPOROZHYE UKR MAGAZIN": "Zaporizhzhia Store (Ukraine)",
        "MAGAZIN ZAPOROZHYE UKR": "Zaporizhzhia Store (Ukraine)",
        "Kompyuterii41": "Zaporizhzhia Store (Ukraine)",
        
        "Spotify AB": "Spotify",
        "Spotify": "Spotify",
        
        "STEAM PURCHASE": "Steam",
        "STEAM Refund": "Steam",
        "Steam": "Steam",
        
        "HoYoverse": "HoYoverse",
        "COGNOSPHERE PTE. LTD": "HoYoverse",
        "MIHOYO LIMITED": "HoYoverse",
        "HoYoverse, Singapore": "HoYoverse",
        
        "RIOT*LOL": "Riot Games",
        "GOOGLE *YOSTAR LIMITED": "Google (Yostar Games)",
        "HS_TowerofFantasy": "Tower of Fantasy (Game)",
        
        "XSOLLA *EPICGAMES": "Xsolla (Epic Games)",
        "XSOLLA /EPICGAMES": "Xsolla (Epic Games)",
        "Xsolla _Twitch": "Xsolla (Twitch)",
        "XSOLLA *TWITCH": "Xsolla (Twitch)",
        "XSOLLA": "Xsolla (Payment Platform)",
        
        # delete after
        "Банк": "OschadBank (fee)",
        
        # PrivatBank
        "На картку": "Transfer to Another Card",
        "Стипендія": "NU Zaporizhzhia Polytechnic: Scholarship",
        "Банкомат Супермаркет Амстор, М ЗАПОРІЖЖЯ, ВУЛ. БОРОДІНСЬКА, БУД. 20 Б": "Terminal (ATM/POS)",
        "Infold Games, SG": "Infold Games",
        "WEB Banking, KYIV": "From Another Card",
        "Запорізька політехніка НУ (інші платежі)": "NU Zaporizhzhia Polytechnic (other payments)",
        "MOBILE BANKING, KYIV": "From Another Card",
    }
    
    # Return the mapped name, or the original name if not found in the mapping
    return vendor_mapping.get(vendor_name, 'unknown')

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
        'січня': '01',
        'лютого': '02',
        'березня': '03',
        'квітня': '04',
        'травня': '05',
        'червня': '06',
        'липня': '07',
        'серпня': '08',
        'вересня': '09',
        'жовтня': '10',
        'листопада': '11',
        'грудня': '12'
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

def import_oschad_csv(file_path: str):
    """
    Import transactions from an Oschad CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
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
        with open(file_path, mode="r", encoding="utf-8-sig", newline='') as file:
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
                    vendor = vendor_raw.strip('*').strip()
                    
                    # Handle the typo in the header: use "decription" if "description" is absent.
                    description = (row.get("description") or row.get("decription") or "").strip()
                    
                    # Get income and debits values.
                    income_str = row.get("income", "").strip()
                    debits_str = row.get("debits", "").strip()
                    
                    # Determine transaction type and amount.
                    if income_str and income_str not in ['*', '']:
                        transaction_type = 'income'
                        amount = Decimal(income_str.replace(',', '.'))
                    elif debits_str and debits_str not in ['*', '']:
                        transaction_type = 'expense'
                        amount = Decimal(debits_str.replace(',', '.'))
                    else:
                        raise ValueError("No valid amount found in row")
                    
                    # Parse balance, if provided.
                    balance_raw = row.get("balance", "").strip()
                    balance_after_transaction = Decimal(balance_raw.replace(',', '.')) if balance_raw else None
                    
                    # Determine category based on vendor.
                    lower_vendor = vendor.lower() if vendor else ''
                    if 'spotify' in lower_vendor:
                        category = 'digital_goods'
                    else:
                        category = 'other'
                    
                    Transaction.objects.create(
                        user=superuser,
                        date=date,
                        card='5167 **** **** 8163',
                        type=transaction_type,
                        amount=amount,
                        currency='UAH',
                        description=description,
                        vendor=vendor,
                        category=category,
                        balance_after_transaction=balance_after_transaction,
                        transaction_source='OschadBank',
                    )
                    success_count += 1
                except KeyError as e:
                    error_messages.append(f"Row {row_number}: Missing required column: {str(e)}")
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
