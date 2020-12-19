from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, permissions, pagination, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
import json
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import *
from .models import *


def is_json(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True
    except ValueError:
        is_valid = False
    return is_valid

# custom permissions for editing models


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "You must be the owner of this content to change it!"

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


# users rest api view for CRUD
class UserAPIView(
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer

    def get_queryset(self):
        request = self.request
        qs = User.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(username__icontains=query)
        return qs


class UserDetailAPIView(
        generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'username'


# posts rest api view for CRUD
class PostAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['featured', 'categories__title']
    search_fields = ('title', 'content', 'categories__title',
                     'author__user__username', 'author__description')

    # def get_queryset(self):
    #     request = self.request
    #     qs = Post.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontains = query)
    #     return qs

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [JSONWebTokenAuthentication]
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
        serializer.delete()

# author rest api view for CRUD


class AuthorAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    pagination_classes = [pagination.LimitOffsetPagination]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['user__username']
    search_fields = ('user__username', 'description')
    ordering_fields = ('id',)

    # def get_queryset(self):
    #     request = self.request
    #     qs = Author.objects.all()
    #     query = request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(description__icontains=query)
    #     return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        for author in Author.objects.filter(user=self.request.user):
            if not author:
                serializer.save(author=self.request.user)


class AuthorDetailAPIView(
        generics.RetrieveAPIView,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    # modify the models to use slugs in future
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, serializer):
        serializer.delete()

    def get_serializer_context(self):
        return {'request': self.request}

# comments rest api view for CRUD


class CommentAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer

    def get_queryset(self):
        request = self.request
        qs = Comment.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(content__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailAPIView(
        generics.RetrieveAPIView,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # modify the models to use slugs in future
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, serializer):
        serializer.delete()

# category rest api view for CRUD
class CategoryAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = CategorySerializer

    def get_queryset(self):
        request = self.request
        qs = Category.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(title__icontains=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoryDetailAPIView(
        generics.RetrieveAPIView,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [SessionAuthentication]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    # modify the models to use slugs in future
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, serializer):
        # do some more checks here first
        serializer.delete()

    def get_serializer_context(self):
        return {'request': self.request}


# contacts rest api view for Creating
class ContactAPIView(
        mixins.CreateModelMixin,
        generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]
    serializer_class = ContactSerializer

    def get_queryset(self):
        request = self.request
        qs = Contact.objects.all()
        query = request.GET.get('q')
        if query is not None:
            qs = qs.filter(description=query)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

