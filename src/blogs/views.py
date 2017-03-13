from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog
from .forms import BlogForm

class BlogView(View):
    def get(self, request, *args, **kwargs):
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
        
        context = {'blogs': blogs}
        template = 'blogs/list.html'
        return render(request, template, context)

class BlogDetailView(View):
    def get(self, request, slug=None, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=slug)
        context = {'blog': blog}
        template = 'blogs/detail.html'
        return render(request, template, context)

class BlogCreateView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        
        form = BlogForm()
        context = {'form': form}
        template = 'blogs/form.html'

        return render(request, template, context)
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()
            message.success(request, "Blog has been successfully created...")
            return HttpResponseRedirect(new_blog.get_abs_url())
        else:
            message.error(request, "Blog was not created successfully...")
            context = {'form': form}
            template = 'blogs/form.html'
            return render(request, template, context)

class BlogUpdateView(View):
    def get(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        
        blog = get_object_or_404(Blog, slug=slug)
        form = BlogForm(instance=blog)
        context = {'form': form}
        template = 'blogs/form.html'
        
        return render(request, template, context)
    
    def post(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        
        blog = get_object_or_404(Blog, slug=slug)
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            messages.success(request, "Blog has been successfully updated...")
            return HttpResponseRedirect(blog.get_abs_url())
        else:
            context = {'form': form}
            template = 'blogs/form.html'
            return render(request, tempalte, context)

class BlogDeleteView(View):
    def get(self, request, slug=None, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        
        blog = get_object_or_404(Blog, slug=slug)
        blog.delete()
        messages.success(request, "Blog has been deleted successfully...")
        return redirect('blogs:list')
