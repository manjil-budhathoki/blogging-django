from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.
class PostListView(ListView):
    '''
    Docstring for PostListView
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'



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

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form field passerd vaidation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )

            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )