# Generated by Django 5.1.5 on 2025-02-03 12:39

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_delete_budget'),
        ('transactions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.CharField(blank=True, choices=[('entertainment', 'Entertainment'), ('digital_goods', 'Digital Goods'), ('food_drink', 'Food & Drink'), ('other', 'Other')], max_length=128, null=True),
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='transaction',
            name='balance_after_transaction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='card',
            field=models.CharField(blank=True, help_text='Card identifier if multiple cards exist', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='currency',
            field=models.CharField(blank=True, help_text='e.g., UAH, USD', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='original_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='original_currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='vendor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, help_text='Amount in card primary currency', max_digits=15),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('expense', 'Expense'), ('income', 'Income')], db_index=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['user', 'date'], name='transaction_user_id_8af7f1_idx'),
        ),
        migrations.AddIndex(
            model_name='transaction',
            index=models.Index(fields=['type', 'date'], name='transaction_type_1ffefc_idx'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
