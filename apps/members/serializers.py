from rest_framework import serializers
from .models import Member, Membership

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'user_id','first_name']

class MembershipSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.first_name', read_only=True)
    
    class Meta:
        model = Membership
        fields = ['id', 'member', 'member_name', 'start_date', 'end_date', 
                 'membership_type', 'amount_paid', 'payment_date']
        