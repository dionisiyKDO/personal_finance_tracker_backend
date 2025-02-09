# import_script.py
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_finance_tracker.settings')
django.setup()

# Now import your models and function
from transactions.utils import import_privat_bank_csv, import_oschad_csv

if __name__ == '__main__':
    file_path = 'oschad.csv'  # adjust path
    success, errors, messages = import_oschad_csv(file_path)
    print(f"Imported {success} transactions with {errors} errors")
    if messages:
        print("\nErrors:")
        for msg in messages:
            print(f"- {msg}")