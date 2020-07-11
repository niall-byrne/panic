"""Pagination for Kitchen Models"""

from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PagePagination(PageNumberPagination):
  page_size = settings.PAGE_SIZE
  max_page_size = settings.PAGE_SIZE_MAX
  page_size_query_param = settings.PAGE_SIZE_PARAM
  page_query_param = settings.PAGE_QUERY_PARAM


class PagePaginationWithOverride(PagePagination):

  def paginate_queryset(self, queryset, request, view=None):
    if request.query_params.get(settings.PAGINATION_OVERRIDE_PARAM):
      return None

    return super().paginate_queryset(queryset, request, view)


class TransactionQueryPagination(PagePagination):
  page_size = settings.PAGE_SIZE_TRANSACTIONS
