import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_finance_tracker.settings")
django.setup()

from transactions.utils import import_privat_bank_csv, import_oschad_csv  # noqa: E402, F401

if __name__ == "__main__":
    file_path = "oschad.csv"
    success, errors, messages = import_oschad_csv(file_path)

    file_path = "privat.csv"
    success, errors, messages = import_privat_bank_csv(file_path)
