from django.conf.urls import url, include
from . import views
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    url(r'rest/', include(router.urls)),
    # url(r'users', views.UserListView.as_view()),
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
