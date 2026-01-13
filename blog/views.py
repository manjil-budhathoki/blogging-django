from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page',1)

    try:
        posts = paginator.page(page_number)
    
    except PageNotAnInteger:
        # If page_number is not an integer get first page of results
        posts = paginator.page(1)

    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, slug):
    '''
        try:
            post = Post.published.get(id=id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
    '''
    
    post = get_object_or_404(
        Post,
        status = Post.Status.PUBLISHED,
        slug = slug,
        published_date__year = year,
        published_date__month = month,
        published_date__day = day
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )