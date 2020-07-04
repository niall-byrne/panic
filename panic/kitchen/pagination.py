"""Pagination for Kitchen Models"""

from django.conf import settings
from rest_framework.pagination import CursorPagination


class BasePagination(CursorPagination):
  ordering = "-name"
  page_size = settings.PAGE_SIZE
  max_page_size = settings.PAGE_SIZE_MAX
  page_size_query_param = settings.PAGE_SIZE_PARAM
  cursor_query_param = settings.CURSOR_QUERY_PARAM


class ItemNamePagination(BasePagination):
  ordering = "-name"


class ShelfPagination(BasePagination):
  ordering = "-name"


class StorePagination(BasePagination):
  ordering = "-name"


class ItemPagination(BasePagination):
  ordering = "-name"


class TransactionQueryPagination(BasePagination):
  ordering = "-date"
