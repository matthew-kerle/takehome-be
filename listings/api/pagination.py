from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_count(self, queryset):
        """
        Override to ensure we're getting the count after all filters are applied.
        """
        return queryset.count()

    def get_paginated_response(self, data):
        """
        Override to ensure count is calculated after all filters are applied.
        """
        response = super().get_paginated_response(data)
        response.data["count"] = self.page.paginator.count
        return response
