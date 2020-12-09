from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 
                'email', 
                'username')
        read_only_fields = ['id']

# for nested user in nested author in posts
class UserInAuthorInPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

# create a serializer for the nested author in posts
class AuthorInPostSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserInAuthorInPostSerializer(read_only=True)
    class Meta:
        model = Author
        fields = ('id',
                  'user',
                  'profile_picture',
                  'uri')
        
    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('author', kwargs={'id': obj.id}, request=request)

# for nested category in posts


class CategoryInPostSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Category
        fields = ('title',
                'uri')

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('category', kwargs={'id': obj.id}, request=request)

class PostSerializer(serializers.ModelSerializer):
    author = AuthorInPostSerializer(read_only=True)
    categories = CategoryInPostSerializer()
    uri = serializers.SerializerMethodField(read_only=True)
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
                'featured',
                'uri')
        read_only_fields = ['id', 'author', 'created_on', 'updated_on']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('post', kwargs={'id': obj.id}, request=request)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 
                'user', 
                'content', 
                'timestamp', 
                'post')
        read_only_fields = ['user', 'id', 'post']

# for nested user in nested author in posts
class UserInAuthorSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ('username',
                'email',
                'uri')

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('user', kwargs={'username': obj.username}, request=request)

# posts belonging to the author nested in the author serializer
class AuthorPostSerializer(serializers.ModelSerializer):
    author = AuthorInPostSerializer(read_only=True)
    categories = CategoryInPostSerializer()
    uri = serializers.SerializerMethodField(read_only=True)
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
                  'featured',
                  'uri')

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('post', kwargs={'id': obj.id}, request=request)

class AuthorSerializer(serializers.ModelSerializer):
    user = UserInAuthorSerializer(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    posts_list = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Author
        fields = ('id', 
                'user', 
                'profile_picture', 
                'profile_bg', 
                'description',
                'uri',
                'posts_list')
        read_only_fields = ['id']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('author', kwargs={'id': obj.id}, request=request)

    def get_posts_list(self, obj):
        request = self.context.get('request')
        postsLimit = 10
        if request:
            limit_query = request.GET.get('postsLimit')
            try:
                postsLimit = int(limit_query)
            except:
                pass
        # equal to Post.objects.filter(author=user)
        qs = obj.post_set.all() 
        return AuthorPostSerializer(qs[:postsLimit], context={'request': request}, many=True).data

class CategorySerializer(serializers.ModelSerializer):
    posts_list = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 
                'title', 
                'thumbnail',
                'uri',
                'posts_list')

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('category', kwargs={'id': obj.id}, request=request)

    def get_posts_list(self, obj):
        request = self.context.get('request')
        postsLimit = 10
        if request:
            limit_query = request.GET.get('postsLimit')
            try:
                postsLimit = int(limit_query)
            except:
                pass
        # qs = Post.objects.filter(categories=obj)
        qs = obj.post_set.all()
        return AuthorPostSerializer(qs[:postsLimit], context={'request': request}, many=True).data

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 
                'name', 
                'email', 
                'message', 
                'timestamp')
        read_only_fields = ['id', 'timestamp']
