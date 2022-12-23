import uuid

from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import get_object_or_404
from django.db.models import Q
from types import NoneType

from service.validators import validate_uuid
from service.paginator import CustomPagination
from service.clear_module import deleter
from .serializers import PetSerializer
from .models import Pets, Photos


class PetsModelViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self, *args, **kwargs):
        obj = self.request.query_params.get("has_photos", "")
        if obj:
            obj_photo = Photos.objects.distinct("pet_id").values_list("pet_id")
            list_id = [
                obj[0].hex for obj in obj_photo if not isinstance(obj[0], NoneType)
            ]
            if obj.lower() == "true":
                return Pets.objects.filter(id__in=list_id)
            if obj.lower() == "false":
                return Pets.objects.filter(~Q(id__in=list_id))
        queryset = Pets.objects.all()
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context_query = Photos.objects.all().values("url", "pet_id", "id")
        context.update({"photo_query": context_query})
        return context

    def add_photo(self, request, id, *args, **kwargs):
        photo = request.FILES.get("binary", False)
        id_uuid = validate_uuid(id)
        if id_uuid and photo:
            obj_pet = get_object_or_404(Pets, id=id_uuid)
            obj_photo = Photos.objects.create(image=photo, pet_id=obj_pet)
            obj_photo.url = (
                "http://localhost:8000/media/" + obj_photo.image.name
            )
            obj_photo.save()
            data = dict(id=obj_photo.id, url=obj_photo.url)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({"error": "Нет фото"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        data = request.data.get("ids", False)
        if data:
            errors, white_list = validate_uuid(data, many=True)
            count_deleted_pet, err_list = deleter(white_list)
            total_err = errors + err_list
            data = dict(deleted=count_deleted_pet, error=total_err)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Нет ids"})
