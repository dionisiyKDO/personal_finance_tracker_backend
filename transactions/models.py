from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("expense", "Expense"),
        ("income", "Income"),
    ]

    # Required fields
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    date = models.DateTimeField(default=timezone.now)
    type = models.CharField(
        max_length=7,
        choices=TRANSACTION_TYPES,
        db_index=True,  # index for frequent filtering
    )
    amount = models.DecimalField(
        max_digits=15, decimal_places=2, help_text="Amount in card primary currency"
    )

    # Optional fields with proper null/blank handling
    card = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Card identifier if multiple cards exist",
    )
    category = models.CharField(
        max_length=128, null=True, blank=True
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    # Currency related fields
    currency = models.CharField(
        max_length=10, null=True, blank=True, help_text="e.g., UAH, USD"
    )
    original_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    original_currency = models.CharField(max_length=10, null=True, blank=True)
    balance_after_transaction = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )

    # Metadata fields
    vendor = models.CharField(max_length=255, null=True, blank=True)
    transaction_source = models.CharField(max_length=100, null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["type", "date"]),
        ]

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M')} - {self.amount} {self.currency or 'N/A'}"

    def save(self, *args, **kwargs):
        if not self.currency and self.original_currency:
            self.currency = self.original_currency
        super().save(*args, **kwargs)
