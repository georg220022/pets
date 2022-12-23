from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):

    default_limit = 20
    page_size_query_param = "limit"
    offset_query_param = "offset"

    def get_paginated_response(self, data):
        return Response({"count": self.count, "items": data})
