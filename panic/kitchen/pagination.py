"""Pagination for Kitchen Models"""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PagePagination(PageNumberPagination):
  page_size = settings.PAGE_SIZE
  max_page_size = settings.PAGE_SIZE_MAX
  page_size_query_param = settings.PAGE_SIZE_PARAM
  page_query_param = settings.PAGE_QUERY_PARAM


class TransactionQueryPagination(PagePagination):
  page_size = settings.PAGE_SIZE_TRANSACTIONS
