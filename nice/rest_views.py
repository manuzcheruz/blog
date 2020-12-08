from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions
from django.shortcuts import get_object_or_404
import json
from rest_framework.authentication import SessionAuthentication
from .serializers import *
from .models import *


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid


class PostAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get_queryset(self):
        request = self.request
        qs = Post.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains = query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            for author in Author.objects.filter(user=self.request.user):
                author = author
        except Author.DoesNotExist:
            author = None
        serializer.save(author=author)


class PostDetailAPIView(
        generics.RetrieveAPIView,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    permission_classes = []
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, serializer):
        # incomplete code but should be able to verify if a user is the owner of the post before deleting
        # try:
        #     for author in Author.objects.filter(user=self.request.user):
        #         if (author.user == self.request.)
        #         author = author
        # except Author.DoesNotExist:
        #     author = None
        serializer.delete()
