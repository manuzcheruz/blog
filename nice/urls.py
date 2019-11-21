from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
    #url(r'^', views.home_page, name="HomePage"),
    # url(r'home/', views.PostList.as_view(), name='home'),
    url(r'^$', views.blog, name='home'),
    # url(r'login/', views.login, name='login'),
    url(r'contact/', views.contact, name='contact'),
    url(r'profile/(?P<pk>\d+)/', views.profile, name='profile'),
    url(r'search/', views.search, name='search'),
    # url(r'bizna', PostCreateView.as_view(), name="bizna"),
    url(r'create/', views.post_create, name='post-create'),
    url(r'post/(?P<pk>\d+)/update/', views.post_update, name='post-update'),
    url(r'post/(?P<pk>\d+)/delete/', views.post_delete, name='post-delete'),
    url(r'category/(?P<pk>\d+)/$', views.category_detail, name='category_detail'),
    url(r'post/(?P<pk>\d+)/', PostDetailView.as_view(), name='buzz'),
    #url(r'buz/(?P<pk>\d+)/update/', PostUpdateView.as_view(), name="update"),
    #url(r'buz/(?P<pk>\d+)/delete/', PostDeleteView.as_view(), name="delete"),
    #url(r'<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]
