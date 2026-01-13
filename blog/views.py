from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
# Create your views here.
def post_list(request):
    post = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': post}
    )

def post_detail(request, id):
    '''
        try:
            post = Post.published.get(id=id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")
    '''
    
    post = get_object_or_404(
        Post,
        id = id,
        status = Post.Status.PUBLISHED
    )

    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )