from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import PostForm

def post_create(request):
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(new_post.get_abs_url())
        else:
            messages.error(request, "Not Successfully Created")
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)

def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'posts/detail.html', context)

def post_list(request):
    if request.user.is_authenticated():
        post_list = Post.objects.all()
    else:
        post_list = Post.objects.active()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'title': 'List',
        'posts': posts
    }
    return render(request, 'posts/list.html', context)

def post_update(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, "Successfully Saved")
        return HttpResponseRedirect(post.get_abs_url())

    context = {
        'title': 'post.title',
        'post': post,
        'form': form
    }
    return render(request, 'posts/form.html', context)

def post_delete(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    post =  get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('posts:list')
