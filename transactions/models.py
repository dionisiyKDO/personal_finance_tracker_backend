from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("expense", "Expense"),
        ("income", "Income"),
    ]
    
    CATEGORY_MAP = {
        "Mobile Service Provider": "Necessary/Mobile",
        "MONO Bank (Ukraine)": "Finance/Banking",
        "Transfer to Another Card": "Finance/Transfers",
        "From Another Card": "Finance/Transfers",
        "NU Zaporizhzhia Polytechnic: Scholarship": "Income/Scholarship",
        "Nova Poshta (Courier Service)": "Shopping/Delivery",
        "Udemy": "Education/Online Courses",
        "Terminal (ATM/POS)": "Finance/ATM",
        "Google play (Duolingo)": "Subscription/Education",
        "Rozetka (Online Store)": "Shopping/OnlineStore",
        "Amazon Prime Video": "Subscription/Entertainment",
        "MooGold (Gaming/Online Service)": "Gaming/Services",
        "Zaporizhzhia Store (Ukraine)": "Shopping/LocalStore",
        "Spotify": "Subscription/Music",
        
        "Steam": "Gaming",
        "Xsolla (Epic Games)": "Gaming",
        "HoYoverse": "Gaming/Gacha",
        "Riot Games": "Gaming/InGameCurrency",
        "Google (Yostar Games)": "Gaming/Gacha",
        "Tower of Fantasy (Game)": "Gaming/Gacha",
        "Infold Games": "Gaming/Gacha",
        
        "Xsolla (Twitch)": "Subscription/Entertainment",
        "Xsolla (Payment Platform)": "Shopping/OnlineStore",
        
        "OschadBank (fee)": "Finance/BankFees",
        "NU Zaporizhzhia Polytechnic (other payments)": "Education/University",
    }
    
    VENDOR_MAP = {
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
        if self.vendor:
            phone_pattern = r"^\+380\d{9}$"
            if re.match(phone_pattern, self.vendor):
                self.vendor = "Mobile Service Provider"
            else:
                self.vendor = self.VENDOR_MAP.get(self.vendor, self.vendor)
            
            # TODO: look what is in category before this
            self.category = self.CATEGORY_MAP.get(self.vendor, "Uncategorized")    
        super().save(*args, **kwargs)
