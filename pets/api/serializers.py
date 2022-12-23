from rest_framework import serializers
from .models import Pets


class PetSerializer(serializers.ModelSerializer):

    photos = serializers.SerializerMethodField()

    class Meta:
        model = Pets
        fields = "__all__"
    
    def get_photos(self, obj):
        ids = str(obj.id)
        data = [
            dict(id=val["id"], url=val["url"])
            for val in self.context["photo_query"]
            if str(val["pet_id"]) == ids
        ]
        if data:
            return data
        return []
