from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True, help_text="When this record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="When this record was last updated")

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    """Customer entity representing a person or organization holding insurance policies."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"


class Policy(TimeStampedModel):
    """Insurance policy linked to a customer."""
    POLICY_TYPES = [
        ("AUTO", "Auto"),
        ("HOME", "Home"),
        ("LIFE", "Life"),
        ("HEALTH", "Health"),
        ("TRAVEL", "Travel"),
        ("OTHER", "Other"),
    ]
    policy_number = models.CharField(max_length=64, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="policies")
    policy_type = models.CharField(max_length=16, choices=POLICY_TYPES, default="OTHER")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    premium = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.policy_number} - {self.policy_type} - {self.customer}"


class Claim(TimeStampedModel):
    """Claim filed against a policy."""
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_REVIEW", "In Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("CLOSED", "Closed"),
    ]
    CLAIM_TYPES = [
        ("ACCIDENT", "Accident"),
        ("THEFT", "Theft"),
        ("DAMAGE", "Damage"),
        ("OTHER", "Other"),
    ]
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name="claims")
    claim_number = models.CharField(max_length=64, unique=True)
    incident_date = models.DateField()
    claim_type = models.CharField(max_length=16, choices=CLAIM_TYPES, default="OTHER")
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="OPEN")

    def __str__(self) -> str:
        return f"{self.claim_number} - {self.status}"
