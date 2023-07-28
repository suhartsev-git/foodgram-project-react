from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class CustomPaginLimitOnPage(PageNumberPagination):
    """
    Кастомный класс пагинации с ограничением количества элементов на странице.
    """
    page_size = settings.SIX_ELEMENTS_ON_PAGE
    page_size_query_param = "limit"
