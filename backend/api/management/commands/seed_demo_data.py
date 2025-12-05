import random
from decimal import Decimal
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from api.models import Customer, Policy, Claim

class Command(BaseCommand):
    """
    Seeds the database with demo data for customers, policies, and claims.
    Ensures idempotency by checking for existing data before creating new entries.
    Includes a --reset flag to clear out existing data before seeding.
    """
    help = 'Seeds the database with demo data for customers, policies, and claims.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing customers, policies, and claims before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Claim.objects.all().delete()
            Policy.objects.all().delete()
            Customer.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared.'))

        fake = Faker()
        customers_created = 0
        policies_created = 0
        claims_created = 0

        # Create Customers
        for _ in range(10):
            email = fake.unique.email()
            if not Customer.objects.filter(email=email).exists():
                Customer.objects.create(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=email,
                    phone=fake.phone_number(),
                    address=fake.address(),
                )
                customers_created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {customers_created} customers.'))

        # Create Policies
        customers = list(Customer.objects.all())
        if customers:
            for _ in range(15):
                policy_number = fake.unique.bothify(text='POL-#########')
                if not Policy.objects.filter(policy_number=policy_number).exists():
                    customer = random.choice(customers)
                    start_date = fake.date_between(start_date='-2y', end_date='today')
                    end_date = start_date + timedelta(days=365)
                    Policy.objects.create(
                        customer=customer,
                        policy_number=policy_number,
                        policy_type=random.choice(['AUTO', 'HOME', 'LIFE']),
                        premium=Decimal(random.uniform(500.0, 5000.0)).quantize(Decimal('0.01')),
                        start_date=start_date,
                        end_date=end_date,
                    )
                    policies_created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {policies_created} policies.'))


        # Create Claims
        policies = list(Policy.objects.all())
        if policies:
            for _ in range(20):
                claim_number = fake.unique.bothify(text='CLM-#########')
                if not Claim.objects.filter(claim_number=claim_number).exists():
                    policy = random.choice(policies)
                    incident_date = fake.date_between(start_date=policy.start_date, end_date=policy.end_date or timezone.now().date())
                    Claim.objects.create(
                        policy=policy,
                        claim_number=claim_number,
                        incident_date=incident_date,
                        claim_type=random.choice(['ACCIDENT', 'THEFT', 'DAMAGE', 'OTHER']),
                        description=fake.sentence(),
                        amount=Decimal(random.uniform(100.0, 20000.0)).quantize(Decimal('0.01')),
                        status=random.choice(['OPEN', 'APPROVED', 'REJECTED']),
                    )
                    claims_created += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully created {claims_created} claims.'))

        self.stdout.write(self.style.SUCCESS('\n--- Seeding Summary ---'))
        self.stdout.write(f'Total Customers: {Customer.objects.count()}')
        self.stdout.write(f'Total Policies: {Policy.objects.count()}')
        self.stdout.write(f'Total Claims: {Claim.objects.count()}')
        self.stdout.write(self.style.SUCCESS('Demo data seeding complete!'))
