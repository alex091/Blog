from django.conf.urls import url
from .views import (
            IndexView,
            CategoryView,
            PostView,
            TagView
            )


app_name = 'posts'

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
    url(r'^tag/(?P<tag>\w+)/$', TagView.as_view(), name='tag'),
    url(r'^(?P<category>[\w-]+)/$', CategoryView.as_view(), name='category'),
    url(r'^(?P<category>[\w-]+)/(?P<post>[\w-]+)/$', PostView.as_view(), name='post'),
]




