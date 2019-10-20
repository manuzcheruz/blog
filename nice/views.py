from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import generic
from .models import *
from .forms import CommentForm, PostForm
#from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.db.models import Count, Q
#from marketing.models import Signup
# Create your views here.


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories__title'))[:4]
    return queryset


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    return render(request, 'nice/categories.html', {'category': category, 'posts': Post.objects.filter(categories=category)[:5], 'post_list_topstories': Post.objects.filter(
        status=1, postview__gte=1).order_by('postview')[0:4], 'counting_cat': Post.objects.values(
        'categories__title').annotate(Count('categories__title'))[:4], 'category_main': Category.objects.all()})


def home_page(request):
    return render(request, 'nice/home.html')


# class PostCreateView(generic.CreateView):
#     model = Post
#     # fields = ['Business_name', 'location', 'Business_type']
#     form_class = PostForm
#     success_url = None

#     def form_valid(self, form):
#             # form.instance.created_by = self.request.user
#             # self.object = form.save()
#         if form.is_valid():
#             form.instance = self.object
#             form.save()

#         return super(PostCreateView, self).form_valid(form)

#     # redirecting the user to the business detail view they just created

#     def get_success_url(self):
#         return reverse_lazy('buzz', kwargs={'pk': self.object.pk})

# class PostCreateView(generic.CreateView):
#     model = Post
#     #template_name = 'post_create.html'
#     form_class = PostForm

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['title'] = 'Create'
#     #     return context

#     def form_valid(self, form):
#         form.instance.author = get_author(self.request.user)
#         # form.save()
#         # return redirect(reverse('buzz', kwargs={
#         #     'pk': form.instance.pk
#         # }))
#         # return super(PostCreateView, self).form_valid(form)
#         return super().form_valid(form)

#     # def get_success_url(self):
#     #     return reverse_lazy('buzz', kwargs={'pk': self.object.pk})


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("buzz", kwargs={
                'pk': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "nice/post_form.html", context)


def post_update(request, pk):
    title = 'Update'
    post = get_object_or_404(Post, id=pk)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("buzz", kwargs={
                'pk': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "nice/post_form.html", context)


def post_delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect(reverse("home2"))

# class PostUpdateView(generic.UpdateView):
#     model = Post
#     template_name = 'nice/post_form.html'
#     form_class = PostForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Update'
#         return context

#     def form_valid(self, form):
#         form.instance.author = get_author(self.request.user)
#         form.save()
#         return redirect(reverse('buzz', kwargs={
#             'pk': form.instance.pk
#         }))


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = '/home2'
    template_name = 'nice/post_confirm_delete.html'


def contact(request):
    return render(request, 'nice/contact.html')


def blog(request):
    category_count = get_category_count()
    # print(category_count)
    category_main = Category.objects.all()
    post_list = Post.objects.filter(
        status=1, featured=True).order_by('-created_on')[:3]
    post_list_dont_miss = Post.objects.filter(
        status=1, featured=True).order_by('-created_on')[:6]
    post_list_latest = Post.objects.filter(
        status=1).order_by('-created_on')[:5]
    post_list_main = Post.objects.filter(
        status=1, featured=True).order_by('-created_on')[0:1]
    post_list_largest = Post.objects.filter(
        status=1).order_by('-created_on')[0:1]
    post_list_topstories = Post.objects.filter(
        status=1, postview__gte=1).order_by('postview')[0:4]
    post_list_trending = Post.objects.filter(
        status=1, postview__gte=1).order_by('postview')[:4]
    posting = Post.objects.all()
    featured = Post.objects.filter(featured=True)
    context = {
        'post_list': post_list,
        'category_main': category_main,
        'post_list_dont_miss': post_list_dont_miss,
        'post_list_trending': post_list_trending,
        'post_list_latest': post_list_latest,
        'post_list_main': post_list_main,
        'post_list_largest': post_list_largest,
        'post_list_topstories': post_list_topstories,
        'posting': posting,
        'category_count': category_count,
        'featured': featured,
    }
    return render(request, 'nice/post_list.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def footer(request):
    if request == 'POST':
        email = request.POST("email")
        #new_signup = Signup()
        new_signup.email = email
        new_signup.save()

# class PostList(generic.ListView):
#     # queryset = Post.objects.filter(status=1).order_by('-created_on')
#     model = Post
#     # template_name = 'nice/home.html'
#     context_object_name = 'Posts'

#     def get_context_data(self, **kwargs):
#         # To use the pk set in Products model to get specific products for individual Post
#         # pk = self.kwargs['pk']
#         # Call the base implementation first to get a context
#         context = super(PostList, self).get_context_data(**kwargs)
#         # Add in a QuerySet of all the books
#         context['post_list'] = Post.objects.filter(
#             status=1).order_by('-created_on')
#         context['post_list_main'] = Post.objects.filter(
#             status=1).order_by('-created_on')[0:1]
#         context['post_list_largest'] = Post.objects.filter(
#             status=1).order_by('-created_on')[0:1]
#         context['post_list_topstories'] = Post.objects.filter(
#             status=1).order_by('-created_on')[0:4]
#         context['posting'] = Post.objects.all()
#         return context


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'nice/post_detail.html'


# class PostDetailView(generic.DetailView):
#     model = Post
#     # paginated_by = 3
#    # form_class = ReviewsForm

#     def get_context_data(self, **kwargs):
#         # first import the global user position variable
#         # global location
#         # To use the pk set in Products model to get specific products for individual Post
#         pk = self.kwargs['pk']
#         # Call the base implementation first to get a context
#         context = super(PostDetailView, self).get_context_data(**kwargs)
#         context['Hotel_list'] = Post.objects.filter(categories='5')
#         # context['Butchery_list'] = Post.objects.filter(Post_type='2')
#         # context['self_list'] = Post.objects.filter(Post_type='4')
#         # context['rental_list'] = Post.objects.filter(Post_type='0')
#         # context['mpesa_list'] = Post.objects.filter(Post_type='6')
#         # context['general_list'] = Post.objects.filter(Post_type='1')
#         return context

class PostDetailView(generic.DetailView):
    model = Post
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
       # most_recent = Post.objects.order_by('-created_on')[:3]
        context = super().get_context_data(**kwargs)
        #context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_main'] = Category.objects.all()
        context['post_list_topstories'] = Post.objects.filter(
            status=1, postview__gte=1).order_by('postview')[0:8]
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("buzz", kwargs={
                'pk': post.pk
            }))
