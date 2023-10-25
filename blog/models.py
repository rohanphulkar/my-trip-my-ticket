from django.db import models
from accounts.models import User
from froala_editor.fields import FroalaField
from django.template.defaultfilters import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = FroalaField(options={
        'height': 400,
        'width': '100%'
    })
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    tags = models.ManyToManyField('Tag', related_name='blog_posts', blank=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        self.slug = slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post.title} - {self.user.email}'
