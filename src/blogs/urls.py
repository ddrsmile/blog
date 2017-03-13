from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.BlogView.as_view(), name='list'),
    url(r'^create/$', views.BlogCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.BlogDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.BlogUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.BlogDeleteView.as_view(), name='delete'),
]
