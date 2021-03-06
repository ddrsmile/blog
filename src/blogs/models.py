from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe

from markdown2 import markdown

class BlogManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(BlogManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    BlogModel = instance.__class__
    # plusing 1 is to make the folder's name equals to instance's id.
    last_blog = BlogModel.objects.order_by("id").last()
    new_id = last_blog.id + 1 if last_blog else 1
    return "{new_id}/{filename}".format(new_id=new_id, filename=filename)

class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True, blank=True,
                              width_field='width_field',
                              height_field='height_field')  
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = BlogManager()

    def __str__(self):
        return self.title

    def get_abs_url(self):
        return reverse('blogs:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        extras = ["code-friendly", "fenced-code-blocks"]
        content = self.content
        marked_content = markdown(content, extras=extras)
        return mark_safe(marked_content)

    class Meta:
        ordering = ['-timestamp', '-updated']

def create_slug(instance, new_slug=None):
    slug = new_slug or slugify(instance.title)
    qs = Blog.objects.order_by("id")
    exists = qs.filter(slug=slug).exists()
    if exists:
        # added instance's id to the slug if the slug is existing.
        new_slug = "{slug}-{num}".format(slug=slug, num=qs.last().id + 1)
        return create_slug(instance=instance, new_slug=new_slug)
    return slug

def pre_save_signal_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    

pre_save.connect(pre_save_signal_receiver, sender=Blog)
