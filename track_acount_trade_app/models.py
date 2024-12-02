# models.py
from django.db import models

class SwapEvent(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    account_address = models.CharField(max_length=44)  # Added field for Solana address
    timestamp = models.DateTimeField()
    token_in_mint = models.CharField(max_length=50)
    token_in_amount = models.DecimalField(max_digits=20, decimal_places=9)
    token_out_mint = models.CharField(max_length=50)
    token_out_amount = models.DecimalField(max_digits=20, decimal_places=9)
    raw_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['account_address']),  # Added index for account address
            models.Index(fields=['timestamp']),
        ]
