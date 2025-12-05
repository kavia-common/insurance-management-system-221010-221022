from rest_framework import serializers
from .models import Customer, Policy, Claim


# PUBLIC_INTERFACE
class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""

    class Meta:
        model = Customer
        fields = "__all__"


# PUBLIC_INTERFACE
class PolicySerializer(serializers.ModelSerializer):
    """Serializer for Policy model with nested customer basic info."""
    customer_detail = CustomerSerializer(source="customer", read_only=True)

    class Meta:
        model = Policy
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "customer_detail")


# PUBLIC_INTERFACE
class ClaimSerializer(serializers.ModelSerializer):
    """Serializer for Claim model with nested policy basic info."""
    policy_detail = PolicySerializer(source="policy", read_only=True)

    class Meta:
        model = Claim
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "policy_detail")
