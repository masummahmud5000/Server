from rest_framework.pagination import LimitOffsetPagination
from .models import Transaction

class trPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20