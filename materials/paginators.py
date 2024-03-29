from rest_framework.pagination import PageNumberPagination


class MaterialPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_paramag = "page_size"
    max_page_size = 10
