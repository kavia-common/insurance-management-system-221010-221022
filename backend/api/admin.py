from django.contrib import admin
from .models import Customer, Policy, Claim


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "created_at")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("created_at",)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "policy_number", "policy_type", "customer", "start_date", "end_date", "premium")
    search_fields = ("policy_number", "customer__first_name", "customer__last_name", "customer__email")
    list_filter = ("policy_type", "start_date", "end_date", "created_at")


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("id", "claim_number", "policy", "status", "incident_date", "amount", "created_at")
    search_fields = ("claim_number", "policy__policy_number", "policy__customer__email")
    list_filter = ("status", "incident_date", "created_at")
