from django import forms

from pagedown.widgets import PagedownWidget

from .models import Blog

class BlogForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = Blog
        fields = [
            'title',
            'content',
            'image',
            'draft',
            'publish'
        ]
