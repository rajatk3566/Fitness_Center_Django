from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from django.db import models

class Member(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=255, default="member")

    def __str__(self):
        return self.first_name


class Membership(models.Model):
    MEMBERSHIP_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='memberships')
    start_date = models.DateField()
    end_date = models.DateField()
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.first_name} - {self.membership_type}"