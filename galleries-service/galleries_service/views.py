from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserPhotoInfo
from .serializers import UserPhotoInfoSerializer

class UserPhotosInfoList(APIView):
    def get(self, request):
        photos_info = UserPhotoInfo.objects.all()
        serializer = UserPhotoInfoSerializer(photos_info, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        serializer = UserPhotoInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserPhotosInfoDetail(APIView):
    def get(self, request, id):
        photo_info = get_object_or_404(UserPhotoInfo, pk=id)
        serializer = UserPhotoInfoSerializer(photo_info)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, id):
        param = get_object_or_404(UserPhotoInfo, pk=id)
        serializer = UserPhotoInfoSerializer(param, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        param = get_object_or_404(UserPhotoInfo, pk=id)
        param.delete()
        return Response('', status.HTTP_204_NO_CONTENT)