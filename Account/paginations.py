from rest_framework.pagination import PageNumberPagination


class FollowerPagination(PageNumberPagination):
    page_size = 10

