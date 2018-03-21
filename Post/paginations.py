from rest_framework import pagination


class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    invalid_page_message = "This page does not exist"


class PostFollowPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = "page"


class PostCommentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class PostVotePagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class StarredPostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'


class FlaggedPostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
