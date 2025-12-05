from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, Policy, Claim
from .serializers import CustomerSerializer, PolicySerializer, ClaimSerializer


@api_view(['GET'])
def health(request):
    """
    Healthcheck endpoint.
    Returns:
      200 OK with {"message": "Server is up!"}
    """
    return Response({"message": "Server is up!"})


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset with common filter backends."""
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


# PUBLIC_INTERFACE
class CustomerViewSet(BaseViewSet):
    """CRUD API for Customers with search and ordering."""
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    filterset_fields = ['email', 'first_name', 'last_name', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'address']
    ordering_fields = ['created_at', 'updated_at', 'first_name', 'last_name']


# PUBLIC_INTERFACE
class PolicyViewSet(BaseViewSet):
    """CRUD API for Policies with search, filter and ordering."""
    queryset = Policy.objects.select_related('customer').all().order_by('-created_at')
    serializer_class = PolicySerializer
    filterset_fields = ['policy_type', 'policy_number', 'customer', 'start_date', 'end_date']
    search_fields = ['policy_number', 'customer__first_name', 'customer__last_name', 'customer__email']
    ordering_fields = ['created_at', 'updated_at', 'start_date', 'end_date', 'premium']


# PUBLIC_INTERFACE
class ClaimViewSet(BaseViewSet):
    """CRUD API for Claims with search, filter and ordering."""
    queryset = Claim.objects.select_related('policy', 'policy__customer').all().order_by('-created_at')
    serializer_class = ClaimSerializer
    filterset_fields = ['status', 'incident_date', 'policy', 'claim_number']
    search_fields = ['claim_number', 'policy__policy_number', 'policy__customer__email']
    ordering_fields = ['created_at', 'updated_at', 'incident_date', 'amount']
