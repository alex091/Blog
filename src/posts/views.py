from . import models
from django.db.models import Count
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, get_list_or_404


class BaseView(TemplateView):
    template_name = ''

    def get_context_data (self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update({
            'categories': models.Category.objects.all(),
            'popular_tags': models.Tag.objects.annotate(used=Count('posts')).order_by('-used')[:15],
            'popular_posts':
                models.Post.objects.filter(created__gte=datetime.now()-timedelta(days=7)).order_by('-visited')[:10],
        })

        return context


class IndexView(BaseView):
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({

            'posts': models.Post.objects.order_by('-created')
        })

        return context


class CategoryView(BaseView):
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category = get_object_or_404(models.Category, slug=kwargs.get('category'))
        context.update({
            'posts': models.Post.objects.filter(category__slug=category).order_by('-created')
        })

        return context


class PostView(BaseView):
    template_name = 'posts/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        instance = get_object_or_404(models.Post, slug=kwargs.get('post'))
        instance.visited += 1
        instance.save()
        tags = models.Tag.objects.filter(posts__id=instance.id)
        context.update({
            'post': instance,
            'tags': tags
        })

        return context


class TagView(BaseView):
    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        context.update({
            'posts': models.Post.objects.filter(tag__slug=kwargs.get('tag')).order_by('-created')
        })

        return context
