from django.db import models
from django.conf import settings
from datetime import timedelta

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
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(auto_now_add=True)

    def renew_membership(self, renewal_type, amount_paid):
        """
        Extend membership based on the renewal type and accumulate amount.
        """

        self.amount_paid += amount_paid
        previous_end_date = self.end_date

        if renewal_type == 'MONTHLY':
            self.end_date += timedelta(days=30)
        elif renewal_type == 'QUARTERLY':
            self.end_date += timedelta(days=120)
        elif renewal_type == 'YEARLY':
            self.end_date += timedelta(days=365)

        self.save()

        MembershipHistory.objects.create(
            member=self.member,
            membership=self,
            renewed_on=self.payment_date,
            previous_end_date=previous_end_date,
            new_end_date=self.end_date,
            renewal_type=renewal_type,
            amount_paid=amount_paid
        )


class MembershipHistory(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='membership_history')
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    renewed_on = models.DateTimeField(auto_now_add=True)
    previous_end_date = models.DateField()
    new_end_date = models.DateField()
    renewal_type = models.CharField(max_length=20, choices=Membership.MEMBERSHIP_CHOICES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.member.first_name} renewed for {self.renewal_type}"
