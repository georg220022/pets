from pets.settings import API_KEY_LIST
from django.http import HttpResponse
from rest_framework import status


def check_api_key(get_response):
    def middleware(request):
        key = request.headers.get("X-API-KEY", False)
        if key not in API_KEY_LIST:
            return HttpResponse(
                "Не авторизованный запрос", status=status.HTTP_401_UNAUTHORIZED
            )
        response = get_response(request)
        return response

    return middleware
