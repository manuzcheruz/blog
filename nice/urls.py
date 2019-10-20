from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    #url(r'^', views.home_page, name="HomePage"),
    # url(r'home/', views.PostList.as_view(), name='home'),
    url(r'home2/', views.blog, name='home2'),
    url(r'contact/', views.contact, name='contact'),
    url(r'search/', views.search, name='search'),
    # url(r'bizna', PostCreateView.as_view(), name="bizna"),
    url('create/', views.post_create, name='post-create'),
    url('post/(?P<pk>\d+)/update/', views.post_update, name='post-update'),
    url('post/(?P<pk>\d+)/delete/', views.post_delete, name='post-delete'),
    url(r'category/(?P<pk>\d+)/$', views.category_detail, name='category_detail'),
    url(r'buz/(?P<pk>\d+)/', PostDetailView.as_view(), name='buzz'),
    #url(r'buz/(?P<pk>\d+)/update/', PostUpdateView.as_view(), name="update"),
    #url(r'buz/(?P<pk>\d+)/delete/', PostDeleteView.as_view(), name="delete"),
    #url(r'<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
