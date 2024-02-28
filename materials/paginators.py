from rest_framework.pagination import PageNumberPagination


class MaterialPaginator(PageNumberPagination):
    page_size = 5
