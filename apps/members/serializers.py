from rest_framework import serializers
from .models import Member, Membership, MembershipHistory


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "user", "first_name"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = request.user  
        return super().create(validated_data)


class MembershipSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.first_name', read_only=True)  
    
    class Meta:
        model = Membership
        fields = ['id', 'member', 'member_name', 'start_date', 'end_date', 
                  'membership_type', 'amount_paid', 'payment_date']


class MembershipRenewSerializer(serializers.Serializer):
    renewal_type = serializers.ChoiceField(choices=Membership.MEMBERSHIP_CHOICES)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2)


class MembershipHistorySerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.first_name', read_only=True)
    membership_type = serializers.CharField(source='membership.membership_type', read_only=True)

    class Meta:
        model = MembershipHistory
        fields = ['id', 'member_id', 'membership_id', 'renewed_on', 'previous_end_date', 
                  'new_end_date', 'renewal_type', 'amount_paid', 'member_name', 'membership_type']


