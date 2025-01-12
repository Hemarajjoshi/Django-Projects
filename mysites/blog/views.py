from django.shortcuts import render, get_object_or_404
from blog.models import Post 
from django.core.paginator import Paginator
from .forms import EmailPostForm,CommentPostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST



# Create your views here.

def post_share(request, post_id):
    post = get_object_or_404(Post, id= post_id, status = Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject =  f'{cd["name"]} recommends you read "{post.title}"'
            message = (
            f' Read "{post.title}"  at {post_url}\n\n'
            f'{cd["name"]}\'s comments: {cd["comments"]}'
            )
            send_mail(
                subject = subject,
                message = message,
                from_email = None ,
                recipient_list = [cd['to']]  
            )

            sent = True
            return  render(request, 'blog/share.html', {'post': post, 'form': form, 'sent': sent})

    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post, 'form':form , 'sent': sent})


def post_list(request):
    post_list = Post.published.all()

    paginator = Paginator(post_list,2)

    page_number = request.GET.get('page', 1)
    
    posts = paginator.page(page_number)
    

    return render(request, 'blog/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status = Post.Status.PUBLISHED)
    comments = post.comments.filter(active = True)
    form = CommentPostForm()
    return render (request, 'blog/details.html', {'post': post, 'comments': comments, 'form': form})



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id = post_id , status = Post.Status.PUBLISHED)
    comment = None
    
    form = CommentPostForm(data = request.POST)
    if form.is_valid :
        comment = form.save(commit = False)
        comment.post = post
        comment.save()
        return render(request, 'blog/comment.html', {'post': post, 'comment': comment, 'form': form})
        










