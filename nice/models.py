from django.db import models
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
from django.urls import reverse

User = get_user_model()


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Test(models.Model):
    testing = models.TextField()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()
    profile_bg = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)
    thumbnail = models.ImageField()

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    categories = models.ManyToManyField(Category)
    #slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    content = HTMLField()
    thumbnail = models.ImageField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    featured = models.BooleanField()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_update_url(self):
        return reverse('update', kwargs={
            'pk': self.pk
        })

    def get_delete_url(self):
        return reverse('delete', kwargs={
            'pk': self.pk
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()
