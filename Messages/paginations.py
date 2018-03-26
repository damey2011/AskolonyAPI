from rest_framework.pagination import PageNumberPagination


class MessageThreadPagination(PageNumberPagination):
    page_size = 10
