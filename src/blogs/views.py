from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog
from .forms import BlogForm

def blog_create(request):
    if not request.user.is_authenticated():
        raise Http404
    form = BlogForm(request.POST or None, request.FILES or None)
    if request.POST:
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()
            messages.success(request, "Successfully Created")
            return HttpResponseRedirect(new_blog.get_abs_url())
        else:
            messages.error(request, "Not Successfully Created")
    context = {
        'form': form
    }
    return render(request, 'blogs/form.html', context)

def blog_detail(request, slug=None):
    blog = get_object_or_404(Blog, slug=slug)
    context = {
        'blog': blog
    }
    return render(request, 'blogs/detail.html', context)

def blog_list(request):
    if request.user.is_authenticated():
        blog_list = Blog.objects.all()
    else:
        blog_list = Blog.objects.active()
    query = request.GET.get('q')
    if query:
        blog_list = blog_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()

    paginator = Paginator(blog_list, 6)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    context = {
        'title': 'List',
        'blogs': blogs
    }
    return render(request, 'blogs/list.html', context)

def blog_update(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    blog = get_object_or_404(blog, slug=slug)
    form = blogForm(request.blog or None, request.FILES or None, instance=blog)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.save()
        messages.success(request, "Successfully Saved")
        return HttpResponseRedirect(blog.get_abs_url())

    context = {
        'title': 'blog.title',
        'blog': blog,
        'form': form
    }
    return render(request, 'blogs/form.html', context)

def blog_delete(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    blog =  get_object_or_404(blog, id=blog_id)
    blog.delete()
    messages.success(request, "Successfully Deleted")
    return redirect('blogs:list')
