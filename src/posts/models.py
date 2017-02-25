from django.db import models
from django.core.urlresolvers import reverse


class Entity(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        abstract = True


class Category(Entity):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('posts:category', kwargs={'category': self.slug})


class Tag(Entity):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def get_absolute_url(self):
        return reverse('posts:tag', kwargs={'tag': self.slug})


def upload_location(instance, filename):
    return '{}/{}'.format(instance.slug, filename)


class Post(Entity):
    content = models.TextField()
    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    visited = models.IntegerField(default=0)
    category = models.ForeignKey(
        to='Category',
        related_name='posts',
        null=False
    )
    tag = models.ManyToManyField(
        to='Tag',
        related_name='posts',
        blank=True
    )

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('posts:post', kwargs={'category': self.category.slug, 'post': self.slug,})
