from rest_framework import pagination


class QuestionPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size = 10
