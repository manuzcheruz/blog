from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 
                'title', 
                'categories', 
                'author', 
                'updated_on', 
                'content', 
                'thumbnail', 
                'created_on', 
                'featured')
        read_only_fields = ['author', 'created_on', 'updated_on']

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'timestamp', 'post')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'thumbnail')

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user', 'profile_picture', 'profile_bg', 'description')

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('id, ''name', 'email', 'message', 'timestamp')