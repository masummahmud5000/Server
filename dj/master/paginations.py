from rest_framework.pagination import PageNumberPagination
# from .models import Transaction

class trPagination(PageNumberPagination):
    page_size = 10
    